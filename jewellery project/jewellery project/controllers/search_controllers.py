from flask import Flask, render_template, render_template_string, request, Blueprint, session, redirect, url_for
from db_config import get_connection

searchbp = Blueprint('Searchallproduct', __name__)



@searchbp.route("/Searchallproduct", methods=['GET', 'POST'])
def Searchallproduct_index():

    conn = get_connection()
    cursor = conn.cursor()

    # Get categories
    cursor.execute("SELECT * FROM JwelleryType")
    categories = cursor.fetchall()

    # Get selected type (POST FIXED)
    if request.method == "POST":
        typeid = request.form.get('typeid')
    else:
        typeid = request.args.get('typeid')

    print("Selected Type:", typeid)

    # Fetch products
    if typeid:
        cursor.execute("SELECT * FROM Products WHERE TypeID=%s", (typeid,))
    else:
        cursor.execute("SELECT * FROM Products")

    itemlist = cursor.fetchall()

    conn.close()

    html_string = """

    <!DOCTYPE html>
    <html lang="en">
    <head>

    <meta charset="UTF-8">
    <title>Jewellery Shop</title>

    <link rel="stylesheet" href="{{ url_for('static', filename='css/bootstrap.min.css') }}">
    <script src="{{ url_for('static', filename='js/bootstrap.bundle.min.js') }}"></script>
    <link href="{{ url_for('static', filename='style.css') }}" rel="stylesheet"/>

    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap" rel="stylesheet">

    <style>

    body{
        font-family:'Poppins',sans-serif;
        background: #FFFFFF;
        margin-top:90px;
    }

    /* TITLE */
    .title{
        text-align:center;
        font-size:40px;
        font-weight:700;
        background: linear-gradient(135deg, #D4AF37, #C5A028);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    /* SEARCH BAR */
    .search-container{
        max-width:700px;
        margin:30px auto;
        background:#fff;
        padding:10px;
        border-radius:50px;
        box-shadow:0 10px 25px rgba(212, 175, 55, 0.1);
        border: 2px solid #F0C75E;
    }

    .search-form{
        display:flex;
        gap:10px;
    }

    .modern-select{
        flex:1;
        border: 2px solid #F0C75E;
        padding:10px;
        border-radius:30px;
        outline:none;
        background: white;
    }

    .modern-select:focus{
        border-color: #D4AF37;
    }

    .btn-search-modern{
        background:linear-gradient(135deg, #D4AF37, #C5A028);
        color:#fff;
        border:none;
        padding:10px 25px;
        border-radius:30px;
    }

    .btn-search-modern:hover{
        background:linear-gradient(135deg, #C5A028, #B8931A);
        box-shadow:0 5px 15px rgba(212, 175, 55, 0.4);
    }

    /* PRODUCT CARD */
    .product-card{
        background:#fff;
        border-radius:20px;
        padding:20px;
        text-align:center;
        box-shadow:0 10px 30px rgba(212, 175, 55, 0.1);
        transition:0.3s;
        border: 2px solid transparent;
    }

    .product-card:hover{
        transform:translateY(-8px);
        box-shadow:0 20px 40px rgba(212, 175, 55, 0.2);
        border-color: #F0C75E;
    }

    .image-box{
        height:200px;
        display:flex;
        justify-content:center;
        align-items:center;
        border-radius:15px;
        background: #FFF9E6;
        overflow: hidden;
    }

    .image-box img{
        max-width:100%;
        max-height:100%;
        transition:0.3s;
    }

    .product-card:hover img{
        transform:scale(1.1);
    }

    .product-title{
        font-size:18px;
        font-weight:600;
        margin-top:10px;
        color: #1a1a2e;
    }

    .price-text{
        font-size:20px;
        font-weight:700;
        background: linear-gradient(135deg, #D4AF37, #C5A028);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .btn-custom{
        display:inline-block;
        margin:5px;
        padding:8px 18px;
        border-radius:25px;
        background:linear-gradient(135deg, #D4AF37, #C5A028);
        color:#fff;
        text-decoration:none;
        transition: all 0.3s ease;
    }

    .btn-custom:hover{
        background:linear-gradient(135deg, #C5A028, #B8931A);
        box-shadow:0 5px 15px rgba(212, 175, 55, 0.4);
        transform: translateY(-2px);
    }

    .out-of-stock{
        position:absolute;
        top:10px;
        right:10px;
        background: linear-gradient(135deg, #D4AF37, #B8931A);
        color:#fff;
        padding:5px 10px;
        border-radius:10px;
        font-size:12px;
    }
🔥 Replace your code with this:

.btn-custom {
    display: inline-block;
    padding: 10px 18px;
    background: linear-gradient(135deg, #111, #333);
    color: #fff;
    border-radius: 8px;
    text-decoration: none;
    font-size: 14px;
    font-weight: 600;
    transition: 0.3s ease;
}

.btn-custom:hover {
    background: linear-gradient(135deg, #333, #000);
    transform: translateY(-2px);
    box-shadow: 0 8px 18px rgba(0,0,0,0.2);
}

/* OUT OF STOCK STYLE */
.out-stock {
    display: inline-block;
    padding: 8px 14px;
    background: #ffe5e5;
    color: #d63031;
    border: 1px solid #ff7675;
    border-radius: 20px;
    font-size: 13px;
    font-weight: 600;
}

/* OPTIONAL DISABLED BUTTON */
.btn-disabled {
    display: inline-block;
    padding: 10px 18px;
    background: #dcdde1;
    color: #636e72;
    border-radius: 8px;
    font-size: 14px;
    cursor: not-allowed;
}

    </style>

    </head>

    <body>

    {% include 'base.html' %}

    <div class="container">

    <h1 class="title">Our Jewellery Collection</h1>

    <!-- SEARCH -->
    <div class="search-container">
        <form method="post" action="/Searchallproduct" class="search-form">

            <select name="typeid" class="modern-select">
                <option value="">All Categories</option>
                {% for c in categories %}
                <option value="{{c['TypeId']}}">{{c['TypeName']}}</option>
                {% endfor %}
            </select>

            <button type="submit" class="btn-search-modern">Search</button>

        </form>
    </div>

    <div class="row">

    {% for row in itemlist %}

    <div class="col-lg-4 col-md-6 mb-4">

    <div class="product-card">

    

    <div class="image-box">
    <img src="{{ url_for('static', filename='uploads/' + row['Photo']) }}">
    </div>

    <h4 class="product-title">{{ row['ProductName'] }}</h4>

    <p class="price-text">₹ {{ row['Weight'] | int *14000 }}</p>

    {% if row['QuantityInStock'] != 0 %}

    <a href="/addtocart?pid={{ row['ProductID'] }}" class="btn-custom">
        🛒 Add to Cart
    </a>

{% else %}

    <span class="out-stock">
        ❌ Out of Stock
    </span>

{% endif %}

    <a href="{{ url_for('Searchallproduct.ProductDetails_index', pid=row['ProductID']) }}" class="btn-custom">View</a>

    </div>

    </div>

    {% endfor %}

    </div>
    </div>

    </body>
    </html>

    """

    return render_template_string(html_string, itemlist=itemlist, categories=categories)



@searchbp.route("/ProductDetails/<int:pid>")
def ProductDetails_index(pid):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Products WHERE ProductID=%s", (pid,))
    item = cursor.fetchone()

    conn.close()

    if not item:
        return "Product not found"

    html_string = """

    <!DOCTYPE html>
    <html>
    <head>

    <link rel="stylesheet" href="{{ url_for('static', filename='css/bootstrap.min.css') }}">
    <link href="{{ url_for('static', filename='style.css') }}" rel="stylesheet"/>

    <style>

    body{
        background: #FFFFFF;
        font-family:'Poppins',sans-serif;
        margin-top:90px;
    }

    .card{
        border-radius:20px;
        box-shadow:0 10px 30px rgba(212, 175, 55, 0.1);
        border: 2px solid #F0C75E;
        background: white;
    }

    .btn-custom{
        background:linear-gradient(135deg, #D4AF37, #C5A028);
        color:#fff;
        border:none;
        padding: 12px 25px;
        border-radius: 25px;
        transition: all 0.3s ease;
    }

    .btn-custom:hover{
        background:linear-gradient(135deg, #C5A028, #B8931A);
        box-shadow:0 5px 15px rgba(212, 175, 55, 0.4);
        transform: translateY(-2px);
    }

    .btn-secondary{
        background: white;
        border: 2px solid #D4AF37;
        color: #D4AF37;
        padding: 12px 25px;
        border-radius: 25px;
        transition: all 0.3s ease;
    }

    .btn-secondary:hover{
        background: #D4AF37;
        color: white;
        box-shadow:0 5px 15px rgba(212, 175, 55, 0.4);
    }

    h2{
        color: #1a1a2e;
        font-weight: 700;
    }

    .out-stock {
        display: inline-block;
        padding: 8px 14px;
        background: #ffe5e5;
        color: #d63031;
        border: 1px solid #ff7675;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 600;
    }

    </style>

    </head>

    <body>

    {% include 'base.html' %}

    <div class="container mt-5">

    <div class="card p-4">

    <div class="row">

    <div class="col-md-6">
    <img src="{{ url_for('static', filename='uploads/' + item['Photo']) }}" class="img-fluid">
    </div>

    <div class="col-md-6">

    <h2>{{ item['ProductName'] }}</h2>

    <p><b>Weight:</b> {{ item['Weight'] }}</p>
    <p><b>Description:</b> {{ item['Description'] }}</p>

    <a href="{{ url_for('Searchallproduct.Searchallproduct_index') }}" class="btn btn-secondary">Back</a>

    {% if item['QuantityInStock'] != 0 %}
    <a href="/addtocart?pid={{ item['ProductID'] }}" class="btn-custom">🛒 Add to Cart</a>
    {% else %}
    <span class="out-stock">
        ❌ Out of Stock
    </span>
    {% endif %}

    </div>

    </div>

    </div>

    </div>

    </body>
    </html>

    """

    return render_template_string(html_string, item=item)


@searchbp.route("/addtocart")
def addtocart():

    pid = request.args.get("pid")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Products WHERE ProductID=%s", (pid,))
    item = cursor.fetchone()

    conn.close()

    if not item:
        return "Item not found"

    cart_item = {
        "id": item["ProductID"],
        "name": item["ProductName"],
        "weight": item["Weight"],
        "photo": item["Photo"],
        "qty": 1
    }

    if "cart" not in session:
        session["cart"] = []

    cart = session["cart"]

    found = False

    for i in cart:
        if i["id"] == int(pid):
            i["qty"] += 1
            found = True
            break

    if not found:
        cart.append(cart_item)

    session["cart"] = cart
    session.modified = True

    return redirect("/showcart")


@searchbp.route("/showcart",methods=["GET","POST"])
def showcart():
    cart = []

    if "cart" in session:
        cart = session["cart"]
    stock_Error = request.args.get('stock_Error')
    # ---------------- FORM ACTION HANDLING ----------------
    if request.method == "POST":
        btn = request.form.get("btn")
        ProductID = int(request.form.get("prod_id"))
        conn = get_connection()
        cursor = conn.cursor()
        itemlist = []
        cursor.execute("SELECT * FROM Products WHERE ProductID=%s", (ProductID,))
        itemlist = cursor.fetchall()

        for item in cart:
            if item["id"] == ProductID:

                if btn == "Increase":
                    if item["qty"] < itemlist[0]["QuantityInStock"]:
                        item["qty"] += 1
                    else:
                        stock_Error = f"the stock {itemlist[0]["ProductName"]} is {itemlist[0]["QuantityInStock"]} so you can  order maximum {itemlist[0]["QuantityInStock"]} items"
                        return redirect(url_for('Searchallproduct.showcart', stock_Error=stock_Error))



                elif btn == "Decrease":
                    if item["qty"] > 1:
                        item["qty"] -= 1

                elif btn == "Remove":
                    cart.remove(item)
                break

        session["cart"] = cart

        return redirect(url_for('Searchallproduct.showcart'))
    grand_total = 0
    labour_total = 0

    for item in cart:
        weight = int(item['weight'])
        qty = item['qty']

        rate = 14000
        labour_rate = 500

        material = weight * rate * qty
        labour = weight * labour_rate * qty

        grand_total += material
        labour_total += labour

    # GST after adding labour
    gst = round((grand_total + labour_total) * 0.05, 2)

    #  Final Amount
    final_total = round(grand_total + labour_total + gst, 2)

    return render_template(
        "cart.html",
        cart=cart,
        stock_Error=stock_Error,
        grand_total=grand_total,
        labour_total=labour_total,
        gst=gst,
        final_total=final_total
    )
