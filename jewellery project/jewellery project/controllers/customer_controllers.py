from flask import Blueprint, render_template, request, redirect
from repositories.Customer_Repository import CustomerRepository

customer_bp = Blueprint("customer", __name__)
repo = CustomerRepository()


@customer_bp.route("/customerlist")
def list_customer():
    customers = repo.get_all()
    return render_template("list_customer.html", customers=customers)


@customer_bp.route("/customer/add", methods=["GET", "POST"])
def add_customer():
    if request.method == "POST":
        repo.add(
            request.form["fname"],
            request.form["lname"],
            request.form["phone"],
            request.form["email"],
            request.form["address"],
            request.form["password"]
        )
        return redirect("/customerlist")

    return render_template("add_customer.html")


@customer_bp.route("/customer/edit/<int:cid>", methods=["GET", "POST"])
def edit_customer(cid):
    if request.method == "POST":
        repo.update(
            cid,
            request.form["fname"],
            request.form["lname"],
            request.form["phone"],
            request.form["email"],
            request.form["address"],
            request.form["password"]
        )
        return redirect("/customerlist")

    customer = repo.get_by_id(cid)
    return render_template("edit_customer.html", customer=customer)


@customer_bp.route("/customer/delete/<int:cid>")
def delete_customer(cid):
    repo.delete(cid)
    return redirect("/customerlist")