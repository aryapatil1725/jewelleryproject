from flask import Blueprint, render_template, request, redirect
from repositories.OrderMaster_Repository import OrderMasterRepository
from repositories.Customer_Repository import CustomerRepository

order_bp = Blueprint("order", __name__)

repo = OrderMasterRepository()
customerrepo = CustomerRepository()


@order_bp.route("/orderlist")
def list_order():
    orders = repo.get_all()
    return render_template("list_order.html", orders=orders)


@order_bp.route("/order/add", methods=["GET", "POST"])
def add_order():
    customerlist = customerrepo.get_all()

    if request.method == "POST":

        cid = request.form["customerid"]
        orderdate = request.form["orderdate"]

        total = float(request.form["total"])
        labour = float(request.form["labour"])
        gst = float(request.form["gst"])
        grand = float(request.form["grand"])

        repo.add(cid, orderdate, total, labour, gst, grand)
        return redirect("/orderlist")

    return render_template("add_order.html", customerlist=customerlist)


@order_bp.route("/order/edit/<int:oid>", methods=["GET", "POST"])
def edit_order(oid):

    customerlist = customerrepo.get_all()
    order = repo.get_by_id(oid)

    if request.method == "POST":

        cid = request.form["customerid"]
        orderdate = request.form["orderdate"]

        total = float(request.form["total"])
        labour = float(request.form["labour"])
        gst = float(request.form["gst"])
        grand = float(request.form["grand"])

        repo.update(oid, cid, orderdate, total, labour, gst, grand)
        return redirect("/orderlist")

    return render_template(
        "edit_order.html",
        order=order,
        customerlist=customerlist
    )


@order_bp.route("/order/delete/<int:oid>")
def delete_order(oid):
    repo.delete(oid)
    return redirect("/orderlist")


