from flask import Blueprint, render_template,request,redirect
from repositories.Customer_Repository import CustomerRepository
from repositories.Product_Repository import ProductRepository
from repositories.OrderMaster_Repository import OrderMasterRepository
from repositories.OrderDetails_Repository import OrderDetailsRepository
from repositories.Payment_Repository import PaymentRepository
from repositories.JwelleryType_Repository import TypeRepository

report_bp = Blueprint("report", __name__)

customerrepo = CustomerRepository()
productrepo = ProductRepository()
orderrepo = OrderMasterRepository()
orderdetailrepo = OrderDetailsRepository()
paymentrepo = PaymentRepository()
typerepo = TypeRepository()



@report_bp.route("/rptcustomer")
def rpt_customer():
    customers = customerrepo.get_all()
    return render_template("reports/rpt_customer.html", customers=customers)



@report_bp.route("/rptproduct")
def rpt_product():
    products = productrepo.get_all()
    return render_template("reports/rpt_product.html", products=products)



@report_bp.route("/rptorder")
def rpt_order():
    orders = orderrepo.get_all()
    return render_template("reports/rpt_order.html", orders=orders)



@report_bp.route("/rptorderdetails")
def rpt_orderdetails():
    details = orderdetailrepo.get_all()
    return render_template("Reports/rpt_orderdetails.html", details=details)

@report_bp.route("/rptpayment")
def rpt_payment():
    payments = paymentrepo.get_all()
    return render_template("reports/rpt_payment.html", payments=payments)

@report_bp.route("/rpttype")
def rpt_type():
    types = typerepo.get_all()
    return render_template("reports/rpt_type.html", types=types)

@report_bp.route("/type_wise_product/<int:typeid>")
def rpt_typewiseproduct(typeid):
    from repositories.Product_Repository import ProductRepository
    repo = ProductRepository()
    products = repo.get_by_type(typeid)
    return render_template("reports/type_wise_product.html", products=products)


@report_bp.route("/customer_wise_order", methods=["GET","POST"])
def customerwise():
    customers = customerrepo.get_all()
    orders = []

    if request.method == "POST":
        cid = request.form["customerid"]
        orders = orderrepo.get_by_customer(cid)

    return render_template(
        "reports/customer_wise_order.html",
        customers=customers,
        orders=orders
    )


@report_bp.route("/date_wise_order", methods=["GET","POST"])
def date_wise_order():

    fdate = request.form.get("fdate")
    tdate = request.form.get("tdate")

    orders = []

    if fdate and tdate:
        orders = orderrepo.date_wise_order(fdate, tdate)

    return render_template(
        "reports/date_wise_order.html",
        orders=orders
    )


@report_bp.route("/date_wise_payment", methods=["GET","POST"])
def date_wise_payment():
    fdate = request.form.get("fdate")
    tdate = request.form.get("tdate")

    payments = []

    if fdate and tdate:
        payments = paymentrepo.date_wise_payment(fdate, tdate)

    return render_template(
        "reports/date_wise_payment.html",
        payments=payments
    )


@report_bp.route("/item_wise_order", methods=["GET","POST"])
def item_wise_order():
    products = productrepo.get_all()
    orders = []

    if request.method == "POST":
        pid = request.form["productid"]
        orders = orderdetailrepo.get_by_product(pid)

    return render_template(
        "reports/item_wise_order.html",
        products=products,
        orders=orders
    )


@report_bp.route("/product_wise_sales", methods=["GET","POST"])
def product_wise_sales():
    products = productrepo.get_all()
    sales = []

    if request.method == "POST":
        pid = request.form["productid"]
        sales = orderdetailrepo.get_sales_by_product(pid)

    return render_template(
        "reports/product_wise_sales.html",
        products=products,
        sales=sales
    )