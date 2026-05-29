
from flask import Blueprint, session, redirect, url_for, render_template
from datetime import datetime
from db_config import get_connection

Checkout = Blueprint('Checkout', __name__)

@Checkout.route("/checkout", methods=["GET", "POST"])
def checkout_index():

    cart = session.get("cart", [])

    if not cart:
        return "Cart is empty"

    # -------- DB CONNECTION ----------
    con = get_connection()
    cur = con.cursor()

    # -------- CALCULATION ----------
    subtotal = 0
    labourcharges = 0

    rate = 14000
    labour_rate = 500   # per gram labour

    for item in cart:
        weight = float(item["weight"])
        qty = int(item["qty"])

        material = weight * rate * qty
        labour = weight * labour_rate * qty

        subtotal += material
        labourcharges += labour

    # GST on (material + labour)
    gst = round((subtotal + labourcharges) * 0.05, 2)

    # Final Total
    grand_total = round(subtotal + labourcharges + gst, 2)

    tot_amt = subtotal

    # -------- GENERATE ORDER ID ----------
    cur.execute("SELECT IFNULL(MAX(OrderID),0)+1 AS oid FROM OrderMaster")
    ord_id = cur.fetchone()["oid"]

    cid = session.get("cid")

    # -------- INSERT ORDER MASTER ----------
    sql_master = """
    INSERT INTO OrderMaster
    (OrderID, CustomerID, OrderDate, TotalAmount, LabourCharges, GSTAmt, GrandTotal)
    VALUES (%s,%s,%s,%s,%s,%s,%s)
    """

    cur.execute(sql_master, (
        ord_id,
        cid,
        datetime.now(),
        tot_amt,
        labourcharges,
        gst,
        grand_total
    ))

    # -------- INSERT ORDER DETAILS ----------
    cur.execute("SELECT IFNULL(MAX(OrderDetailID),0) AS did FROM OrderDetails")
    sr = cur.fetchone()["did"] + 1

    for item in cart:
        weight = float(item["weight"])
        qty = int(item["qty"])
        pid=int(item["id"])

        amt = weight * rate * qty

        sql_details = """
        INSERT INTO OrderDetails
        (OrderDetailID, OrderID, ProductID, Quantity, Rate, Subtotal)
        VALUES (%s, %s, %s, %s, %s, %s)
        """

        cur.execute(sql_details, (
            sr,
            ord_id,
            item["id"],
            qty,
            rate,
            amt
        ))

        sr += 1
        cur.execute("update products set QuantityInStock=QuantityInStock-%s where ProductID=%s",(qty,pid))
        con.commit()

    # -------- COMMIT ----------
    con.commit()
    con.close()

    # -------- SAVE FOR PAYMENT ----------
    session["ordid"] = ord_id
    session["amt"] = subtotal
    session["labour"] = labourcharges
    session["gstamt"] = gst
    session["grand"] = grand_total

    # -------- CLEAR CART ----------
    session["cart"] = []
    session.modified = True

    return redirect("/Payment1")

from flask import Blueprint, session, request, redirect, render_template
from datetime import datetime


Payment = Blueprint('Payment', __name__)

@Payment.route("/Payment1", methods=["GET", "POST"])
def payment():

    # -------- SESSION ----------
    ordid = session.get("ordid")
    amount = session.get("grand")

    con = get_connection()
    cur = con.cursor()

    # -------- GET ORDER LIST ----------
    cur.execute("SELECT OrderID FROM OrderMaster")
    orderlist = cur.fetchall()

    if request.method == "POST":

        # -------- FORM DATA ----------
        payment_mode = request.form.get("method")
        payment_date = request.form.get("paymentdate")
        order_id = request.form.get("orderid")
        amt = request.form.get("amount")

        # -------- GENERATE PAYMENT ID ----------
        cur.execute("SELECT IFNULL(MAX(PaymentID),0)+1 AS pid FROM Payment")
        result = cur.fetchone()
        pid = result["pid"]

        # -------- INSERT PAYMENT ----------
        sql = """
        INSERT INTO Payment
        (PaymentID, OrderID, PaymentDate, AmountPaid, PaymentMethod)
        VALUES (%s,%s,%s,%s,%s)
        """

        cur.execute(sql, (
            pid,
            order_id,
            payment_date,
            amt,
            payment_mode
        ))

        con.commit()
        con.close()

        # -------- CLEAR SESSION ----------
        session.pop("ordid", None)
        session.pop("grand", None)

        return redirect(url_for('Payment.Invoice', pid=pid))

    con.close()

    return render_template(
        "Payment1.html",
        ordid=ordid,
        amount=amount,
        orderlist=orderlist,
        today=datetime.now().strftime("%Y-%m-%d")
    )
@Payment.route("/Invoice", methods=["GET"])
def Invoice():

    con = get_connection()
    cur = con.cursor()

    pid = request.args.get("pid")

    # ---------------- PAYMENT ----------------
    cur.execute("SELECT * FROM payment WHERE PaymentID=%s", (pid,))
    paymentdata = cur.fetchall()

    if not paymentdata:
        return "Invalid Payment ID"

    order_id = paymentdata[0]["OrderID"]

    # ---------------- ORDER MASTER ----------------
    cur.execute("SELECT * FROM ordermaster WHERE OrderID=%s", (order_id,))
    orderMaster = cur.fetchall()

    # ---------------- ORDER DETAILS ----------------
    cur.execute("""
        select OrderDetailID,
        products.ProductName,TypeName,Quantity,
        Rate,Subtotal 
        from orderdetails,products,jwellerytype 
        where orderdetails.ProductID=products.ProductID 
        and products.TypeID=jwellerytype.TypeID 
        and orderdetails.OrderID=%s
    """, (order_id,))

    order_details = cur.fetchall()

    if not order_details:
        return "No order details found"

    # ---------------- CUSTOMER ----------------
    cust_id = orderMaster[0]["CustomerID"]   # correct index after SELECT
    cur.execute("SELECT * FROM customer WHERE CustomerID=%s", (cust_id,))
    cust_data = cur.fetchall()

    con.close()

    return render_template(
        "Invoice.html",
        paymentdata=paymentdata,
        orderMaster=orderMaster,
        order_details=order_details,
        cust_data=cust_data
    )