import os
from flask import Blueprint, render_template, request, redirect, current_app, flash
from repositories.Product_Repository import ProductRepository
from repositories.JwelleryType_Repository import TypeRepository

product_bp = Blueprint("product", __name__)
repo = ProductRepository()
typerepo = TypeRepository()
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def ensure_upload_folder():
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)


@product_bp.route("/productlist")
def list_product():
    products = repo.get_all()
    return render_template("list_product.html", products=products)


@product_bp.route("/product/add", methods=["GET", "POST"])
def add_product():
    typelist = typerepo.get_all()

    if request.method == "POST":
        photo1 = ""
        file = request.files.get('photo1')

        if file and file.filename != "" and allowed_file(file.filename):
            # Ensure upload folder exists
            ensure_upload_folder()
            
            # Secure the filename and save
            filename = file.filename
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            
            # Get absolute path based on current working directory
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            full_filepath = os.path.join(base_dir, filepath)
            
            file.save(full_filepath)
            photo1 = filename
        else:
            photo1 = request.form.get('existing_photo', '')

        repo.add(
            request.form["pname"],
            request.form["typeid"],
            request.form["gender"],
            request.form["weight"],
            request.form["qty"],
            request.form["desc"],
            photo1
        )

        return redirect("/productlist")

    return render_template("add_product.html", typelist=typelist)


@product_bp.route("/type_wise_product")
def type_wise_product():
    typelist = typerepo.get_all()
    typeid = request.args.get("typeid")

    products = []

    if typeid:
        products = repo.get_by_type(typeid)

    return render_template(
        "reports/type_wise_product.html",
        typelist=typelist,
        products=products
    )
@product_bp.route("/product/edit/<int:pid>", methods=["GET", "POST"])
def edit_product(pid):
    product = repo.get_by_id(pid)
    typelist = typerepo.get_all()

    if request.method == "POST":
        pname = request.form["pname"]
        typeid = request.form["typeid"]
        gender = request.form["gender"]
        weight = float(request.form["weight"])
        qty = int(request.form["qty"])
        desc = request.form["desc"]
        
        # Handle photo upload
        photo = ""
        file = request.files.get('photo1')
        
        if file and file.filename != "" and allowed_file(file.filename):
            # Ensure upload folder exists
            ensure_upload_folder()
            
            # Get absolute path based on current working directory
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            filename = file.filename
            filepath = os.path.join(base_dir, UPLOAD_FOLDER, filename)
            
            file.save(filepath)
            photo = filename
        else:
            # Keep existing photo
            photo = request.form.get('existing_photo', '')
        
        repo.update(pid, pname, typeid, gender, weight, qty, desc, photo)

        return redirect("/productlist")

    return render_template("edit_product.html", product=product, typelist=typelist)
@product_bp.route("/product/delete/<int:id>")
def delete_product(id):
    try:
        repo.delete(id)
        flash("Product deleted successfully!", "success")
    except Exception as e:
        # Check if it's a foreign key constraint error
        if "foreign key constraint fails" in str(e).lower():
            flash("Cannot delete this product! It has associated orders. Delete the related orders first.", "danger")
        else:
            flash(f"Error deleting product: {str(e)}", "danger")
    return redirect("/productlist")
