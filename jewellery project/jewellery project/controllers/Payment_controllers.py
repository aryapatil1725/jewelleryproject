from flask import Blueprint, render_template, request, redirect
from repositories.Payment_Repository import PaymentRepository
from repositories.OrderMaster_Repository import OrderMasterRepository

payment_bp = Blueprint("payment", __name__)

repo = PaymentRepository()
orderrepo = OrderMasterRepository()


@payment_bp.route("/paymentlist")
def list_payment():
    payments = repo.get_all()
    return render_template("list_payment.html", payments=payments)


@payment_bp.route("/payment/add", methods=["GET", "POST"])
def add_payment():
    orderlist = orderrepo.get_all()

    if request.method == "POST":
        orderid = request.form["orderid"]
        paymentdate = request.form["paymentdate"]
        amount = float(request.form["amount"])
        method = request.form["method"]

        repo.add(orderid, paymentdate, amount, method)
        return redirect("/paymentlist")

    return render_template("add_payment.html", orderlist=orderlist)



@payment_bp.route("/payment/edit/<int:id>", methods=["GET", "POST"])
def edit_payment(id):
    orderlist = orderrepo.get_all()
    payment = repo.get_by_id(id)

    if request.method == "POST":
        orderid = request.form["orderid"]
        paymentdate = request.form["paymentdate"]
        amount = float(request.form["amount"])
        method = request.form["method"]

        repo.update(id, orderid, paymentdate, amount, method)
        return redirect("/paymentlist")

    return render_template("edit_payment.html",
                           payment=payment,
                           orderlist=orderlist)


@payment_bp.route("/payment/delete/<int:id>")
def delete_payment(id):
    repo.delete(id)
    return redirect("/paymentlist")