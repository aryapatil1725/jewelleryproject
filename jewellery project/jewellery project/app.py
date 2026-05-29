from flask import Flask
from controllers.type_controllers import type_bp
from controllers.customer_controllers import customer_bp
from controllers.Payment_controllers import payment_bp
from controllers.product_controllers import product_bp
from controllers.OrderDetails_controllers import orderdetail_bp
from controllers.OrderMaster_controllers import order_bp
from controllers.home_controllers import home_bp
from controllers.report_controllers import report_bp
from controllers.search_controllers import searchbp
from controllers.checkout_controller import Checkout, Payment

app = Flask(__name__)

app.register_blueprint(home_bp)
app.register_blueprint(order_bp)
app.register_blueprint(type_bp)
app.register_blueprint(customer_bp)
app.register_blueprint(payment_bp)
app.register_blueprint(product_bp)
app.register_blueprint(orderdetail_bp)
app.register_blueprint(report_bp)
app.register_blueprint(searchbp)
app.register_blueprint(Checkout)
app.register_blueprint(Payment)

app.secret_key = "abc123"

if __name__ == "__main__":
    app.run(debug=True)