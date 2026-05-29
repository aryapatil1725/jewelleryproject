from flask import Blueprint, render_template, request, redirect, session, url_for
import pymysql

from db_config import get_connection

home_bp = Blueprint("home", __name__)

@home_bp.route("/")
def home():
    return render_template("home.html")


@home_bp.route('/login', methods=['GET', 'POST'])
def AdminLogIn_index():
    error = ""

    if request.method == "POST":
        username = request.form.get("Username")
        password = request.form.get("password")

        if username == "admin" and password == "123":
            session["islogin"] = True
            return render_template("AdminDashboard.html")
        else:
            error = "Invalid email or password"

    return render_template("adminlogin.html", error=error)


@home_bp.route('/AdminDashboard')
def AdminDashboard():
    return render_template("AdminDashboard.html")


@home_bp.route('/custamerlogin', methods=['GET', 'POST'])
def custamer_index():
    error = ""

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        conn = get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            "SELECT * FROM Customer WHERE Email=%s AND Password=%s",
            (email, password)
        )

        user = cursor.fetchone()
        conn.close()

        if user:
            session['cid'] = user['CustomerID']
            session['cnm'] = user['FirstName']
            return render_template("custamer.html", user=user)
        else:
            error = "Invalid email or password"

    return render_template("custamerlogin.html", error=error)


@home_bp.route('/customerregister', methods=['GET', 'POST'])
def customer_register():
    reg_error = ""
    success = ""

    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        phone = request.form.get("phone")
        address = request.form.get("address")

        # Validate password match
        if password != confirm_password:
            reg_error = "Passwords do not match"
        else:
            conn = get_connection()
            cursor = conn.cursor(pymysql.cursors.DictCursor)

            # Check if email already exists
            cursor.execute(
                "SELECT * FROM Customer WHERE Email=%s",
                (email,)
            )
            existing_user = cursor.fetchone()

            if existing_user:
                reg_error = "Email already registered. Please use a different email."
            else:
                # Split name into first name and last name
                name_parts = name.split(maxsplit=1)
                fname = name_parts[0]
                lname = name_parts[1] if len(name_parts) > 1 else ""

                # Insert new customer
                cursor.execute(
                    "INSERT INTO Customer (FirstName, LastName, Phone, Email, Address, Password) VALUES (%s, %s, %s, %s, %s, %s)",
                    (fname, lname, phone, email, address, password)
                )
                conn.commit()
                success = "Registration successful! Please login with your credentials."

            conn.close()

    return render_template("custamerlogin.html", reg_error=reg_error, success=success)


@home_bp.route('/custamerDashboard')
def custamerDashboard():
    return render_template("custamer.html")


@home_bp.route('/myorders')
def my_orders():
    cid = session.get("cid")

    if not cid:
        return redirect(url_for('home.custamer_index'))

    conn = get_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    # -------- ORDER MASTER ----------
    cursor.execute("""
        SELECT * FROM OrderMaster 
        WHERE CustomerID=%s
        ORDER BY OrderDate DESC
    """, (cid,))
    orders = cursor.fetchall()

    # -------- ORDER DETAILS ----------
    for order in orders:
        cursor.execute("""
            SELECT 
                od.Quantity,
                od.Rate,
                od.Subtotal,
                p.ProductName,
                p.Photo
            FROM OrderDetails od
            JOIN Products p ON od.ProductID = p.ProductID
            WHERE od.OrderID=%s
        """, (order['OrderID'],))

        order['items'] = cursor.fetchall()

    conn.close()

    return render_template("myorders.html", orders=orders)