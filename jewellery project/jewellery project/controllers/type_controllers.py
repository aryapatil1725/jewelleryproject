from flask import Blueprint, render_template, request, redirect
from repositories.JwelleryType_Repository import TypeRepository

type_bp = Blueprint("type", __name__)
repo = TypeRepository()


@type_bp.route("/typelist")
def list_type():
    types = repo.get_all()
    return render_template("list_type.html", types=types)


@type_bp.route("/type/add", methods=["GET", "POST"])
def add_type():
    if request.method == "POST":
        repo.add(request.form["typename"])
        return redirect("/typelist")

    return render_template("add_type.html")


@type_bp.route("/type/edit/<int:tid>", methods=["GET", "POST"])
def edit_type(tid):
    if request.method == "POST":
        repo.update(tid, request.form["typename"])
        return redirect("/typelist")

    type_data = repo.get_by_id(tid)
    return render_template("edit_type.html", type=type_data)


@type_bp.route("/type/delete/<int:tid>")
def delete_type(tid):
    repo.delete(tid)
    return redirect("/typelist")