from flask import Blueprint, render_template, request, redirect
from repositories.OrderDetails_Repository import OrderDetailsRepository
from repositories.Product_Repository import ProductRepository
from repositories.OrderMaster_Repository import OrderMasterRepository

orderdetail_bp = Blueprint("orderdetail", __name__)

repo = OrderDetailsRepository()
productrepo = ProductRepository()
orderrepo = OrderMasterRepository()


@orderdetail_bp.route("/orderdetailslist")
def list_orderdetails():
    details = repo.get_all()
    return render_template("list_orderdetails.html", details=details)


@orderdetail_bp.route("/orderdetails/add", methods=["GET", "POST"])
def add_orderdetails():
    productlist = productrepo.get_all()
    orderlist = orderrepo.get_all()

    if request.method == "POST":
        orderid = request.form["orderid"]
        productid = request.form["productid"]

        qty = float(request.form["qty"])
        rate = float(request.form["rate"])
        subtotal = qty * rate

        repo.add(orderid, productid, qty, rate, subtotal)
        return redirect("/orderdetailslist")

    return render_template(
        "add_orderdetails.html",
        productlist=productlist,
        orderlist=orderlist
    )


@orderdetail_bp.route("/orderdetails/edit/<int:id>", methods=["GET", "POST"])
def edit_orderdetails(id):
    productlist = productrepo.get_all()
    orderlist = orderrepo.get_all()
    detail = repo.get_by_id(id)

    if request.method == "POST":
        orderid = request.form["orderid"]
        productid = request.form["productid"]

        qty = float(request.form["qty"])
        rate = float(request.form["rate"])
        subtotal = qty * rate

        repo.update(id, orderid, productid, qty, rate, subtotal)
        return redirect("/orderdetailslist")

    return render_template(
        "edit_orderdetails.html",
        detail=detail,
        productlist=productlist,
        orderlist=orderlist
    )


@orderdetail_bp.route("/orderdetails/delete/<int:id>")
def delete_orderdetails(id):
    repo.delete(id)
    return redirect("/orderdetailslist")