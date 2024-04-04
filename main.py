import pandas as pd
import stripe, os
from random import randint
from flask import Flask, abort, render_template, redirect, url_for, request, flash, jsonify
from flask_bootstrap import Bootstrap5
from forms import ContactForm, LoginForm, RegisterForm, ShippingForm, OrderQuantity
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from feeders import populate_product_table
from backofshop import contact_email, order_confirmation_email

EMPTY_CART = True
CUSTOMER_CART = []
ORDER_DETAILS = [" Item  ------------------------------  Price  -  Quantity "]
ORDER_TOTAL = 0
SHIPPING_ADDRESS = []

stripe_keys = {
    "secret_key": os.environ.get("STRIPE_SECRET_KEY"),
    "publishable_key": os.environ.get("STRIPE_PUBLISHABLE_KEY"),
}

stripe.api_key = stripe_keys["secret_key"]

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("app_secret_key")
bootstrap = Bootstrap5(app)

# Flask Login
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)


# Log In Required decorator function
def login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.is_authenticated == False:
            return abort(403)
        return func(*args, **kwargs)
    return decorated_function


### DATABASE CREATION & TABLES ###
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///onlineshop.db?charset=utf8mb4'
db = SQLAlchemy()
db.init_app(app)


## insect table ##
class Products(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.String(10), unique=True)
    productname = db.Column(db.String(100))
    short_name = db.Column(db.String(50))
    image_link = db.Column(db.String(100))
    price = db.Column(db.String(10))
    rating = db.Column(db.String(10))
    reviews = db.Column(db.String(10))
    short_desc = db.Column(db.String(100))
    quantity = db.Column(db.String(50))
    description = db.Column(db.String(1250))
    cart_name = db.Column(db.String(100))
   

## user table ##
class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50))
    lastname = db.Column(db.String(100))
    fullname = db.Column(db.String(150))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))

    customer_cart = relationship("ShoppingCart", back_populates="customer")

## cart table ##
class ShoppingCart(db.Model):
    __tablename__ = "shoppingcart"
    id = db.Column(db.Integer, primary_key=True)
    
    customer_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    customer = relationship("User", back_populates="customer_cart")
        
    item_id = db.Column(db.String(10))
    productname = db.Column(db.String(100))
    price = db.Column(db.String(10))
    cart_name = db.Column(db.String(100))
    quantity = db.Column(db.Integer)

with app.app_context():
    db.create_all()

populate_product_table(table=Products)

# Lists create 'cards' for shop and item pages
list_of_items = []
df = pd.read_sql_table("products", con="sqlite:///./instance/onlineshop.db")
for index, product in df.iterrows():
    product_details = [product.item_id, product.productname, product.short_name, product.image_link, product. price, product.rating, product.reviews, product.short_desc, product.quantity, product.description]
    list_of_items.append(product_details)


### FLASK WEB ROUTES ###
## splash home page ##
@app.route("/")
def home():
    return render_template("index.html")


## shop home ##
@app.route("/shophome")
def shophome():
    item_cards = list_of_items
    return render_template("shop.html", item_cards=item_cards)


## selected item ##
@app.route("/item/<item_id>", methods=["GET","POST"])
def item(item_id):
    quantity = OrderQuantity()
    for index in range(len(list_of_items)):
        if list_of_items[index][0] == item_id:
            item = list_of_items[index]

    if request.method == "POST":
        selected_item = db.session.execute(db.select(Products).where(Products.item_id == item_id)).scalar()
        selected_cart_item = None
        user_cart_item_ids = []
        cart_items = pd.read_sql_table("shoppingcart", con="sqlite:///./instance/onlineshop.db")
        
        # Creates list of unique ids in ShoppingCart tied to currently signed in user
        for index, product in cart_items.iterrows():
            if cart_items.customer_id[index] == current_user.id:
                user_cart_item_ids.append(product.id)
        # Compares user_cart_item_ids with entries in ShoppingCart table. If there is a match, value is assigned to product_in_cart
        for item_id in user_cart_item_ids:
            product_in_cart = db.session.execute(db.select(ShoppingCart).where(ShoppingCart.id == item_id)).scalar()
            # If the product_in_cart matches selected_item, selected_cart_item's value is updated
            if selected_item.item_id == product_in_cart.item_id:
                selected_cart_item = product_in_cart
        # If selected-cart_item was updated to a DB entry, then item exists in cart and quantity is updated
        if selected_cart_item != None:
            new_quantity = int(request.form.get("quantity_dropdown"))
            selected_cart_item.quantity = new_quantity
            db.session.commit()
        # If selected_cart_item remains None, then item does not exist in the user's cart and is added
        else:
            add_to_cart = ShoppingCart(
                customer = current_user,
                item_id = selected_item.item_id,
                productname = selected_item.productname,
                price = selected_item.price,
                cart_name = selected_item.cart_name,
                quantity = int(request.form.get("quantity_dropdown")),
            )
            db.session.add(add_to_cart)
            db.session.commit()

        return redirect(url_for("cart"))

    return render_template("item.html", quantity=quantity, item=item)


## login ##
@app.route("/login", methods=["GET","POST"])
def login():
    login_form = LoginForm()

    with app.app_context():
        result = db.session.execute(db.select(User)).fetchall()

    if current_user.is_authenticated == True:
        return redirect(url_for("shophome"))
    
    if request.method == "POST":
        email = request.form.get("email").lower()
        password = request.form.get("password")
        result = db.session.execute(db.select(User).where(User.email==email))
        user = result.scalar()

        if not user:
            flash("That email does not exist in our system. Please try again or register.")
            return redirect(url_for("login"))
        
        elif not check_password_hash(user.password, password):
            flash("Incorrect password. Please try again.")
            return redirect(url_for("login"))

        else:
            login_user(user)
            return redirect(url_for("shophome"))

    return render_template("login.html", login_form=login_form)


## register ##
@app.route("/register", methods=["GET","POST"])
def register():
    register_form = RegisterForm()

    if current_user.is_authenticated == True:
        return redirect(url_for("shophome"))
    
    if register_form.validate_on_submit():
        email = request.form.get("email").lower()
        result = db.session.execute(db.select(User).where(User.email == email))
        user = result.scalar()

        if user:
            flash("An account has already been registered with this email. Please log in or use a different email.")
            return redirect(url_for("register"))
        
        if request.form.get("password") != request.form.get("confirm_password"):
            flash("Passwords do not match. Please make sure that both password fields match!")
            return redirect(url_for("register"))

        plaintext_password = request.form.get("confirm_password")
        hashed_password = generate_password_hash(
            password = plaintext_password,
            method="pbkdf2:sha256",
            salt_length = 8
            )
        new_user = User(
            firstname = request.form.get("firstname").title(),
            lastname = request.form.get("lastname").title(),
            fullname = request.form.get("firstname").title() + " " + request.form.get("lastname").title(),
            email = request.form.get("email").lower(),
            password = hashed_password
        )
        
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)

        return redirect(url_for("shophome"))

    return render_template("register.html", register_form=register_form, current_user = current_user.is_authenticated)


## logout ##
@app.route("/logout")
def logout():
    if current_user.is_authenticated == False:
        return redirect(url_for("login"))

    logout_user()
    return render_template("logout.html")


## cart ##
@app.route("/cart")
@login_required
def cart():
    global EMPTY_CART, CUSTOMER_CART, ORDER_DETAILS, ORDER_TOTAL
    EMPTY_CART = True
    CUSTOMER_CART = []
    ORDER_DETAILS = [" Item  ------------------------------  Price  -  Quantity "]
    ORDER_TOTAL = 0
    cart_item = []
    cart_df = pd.read_sql_table("shoppingcart", con="sqlite:///./instance/onlineshop.db")
    
    for index, product in cart_df.iterrows():
        if cart_df.customer_id[index] == current_user.id:
            cart_item = [product.item_id, product.cart_name, product.price, product.quantity]
            CUSTOMER_CART.append(cart_item)

    # Calculates cart total    
    for item in CUSTOMER_CART:
        item_price = float(item[2]) * item[3]
        ORDER_TOTAL += item_price

    ORDER_TOTAL = round(ORDER_TOTAL, 2)

    if len(CUSTOMER_CART) >= 1:
        EMPTY_CART = False
    elif len(CUSTOMER_CART) == 0:
        EMPTY_CART = True
    
    for item in CUSTOMER_CART:
        ORDER_DETAILS.append(f"{item[1]} - ${item[2]} - {item[3]}")
    
    ORDER_DETAILS.append(f"Order Total: ${ORDER_TOTAL}")
    
    return render_template("cart.html", customer_cart=CUSTOMER_CART, empty_cart=EMPTY_CART, order_total=ORDER_TOTAL)


## Update Item ##
@app.route("/update")
def update():
    try:
        item_name = request.args.get("item_name")
        selected_item = db.session.execute(db.select(Products).where(Products.cart_name == item_name)).scalar()
        item_id = selected_item.item_id
        
        return redirect(url_for("item", item_id=item_id))
    
    except:
        abort(404)


## Remove Item ##
@app.route("/remove")
def remove():
    try:
        item_name = request.args.get("item_name")
        delete_from_cart = db.session.execute(db.select(ShoppingCart).where(ShoppingCart.cart_name == item_name)).scalar()
        db.session.delete(delete_from_cart)
        db.session.commit()

        return redirect(url_for("cart"))
    
    except:
        abort(404)


## shipping ##
@app.route("/shipping", methods=["GET","POST"])
@login_required
def shipping():
    global EMPTY_CART, SHIPPING_ADDRESS
    SHIPPING_ADDRESS = []
    shipping_form = ShippingForm()

    if EMPTY_CART == True:
        return redirect(url_for("shophome"))
    
    if request.form.get("back"):
        return redirect(url_for("cart"))
    
    if shipping_form.validate_on_submit():

        shipping_firstname = request.form.get("firstname")
        shipping_lastname = request.form.get("lastname")
        shipping_email = request.form.get("email")
        shipping_phone = request.form.get("phone")
        shipping_address_line1 = request.form.get("addressline1")
        shipping_address_line2 = request.form.get("addressline2")
        shipping_city = request.form.get("city")
        shipping_state = request.form.get("state")
        shipping_zipcode = request.form.get("zipcode")
        
        SHIPPING_ADDRESS.append("")
        SHIPPING_ADDRESS.append("Shipping Address")
        SHIPPING_ADDRESS.append(f"{shipping_firstname} {shipping_lastname}")
        SHIPPING_ADDRESS.append(f"{shipping_address_line1}")
        if shipping_address_line2 != "":
            SHIPPING_ADDRESS.append(f"{shipping_address_line2}")
        SHIPPING_ADDRESS.append(f"{shipping_city}, {shipping_state} {shipping_zipcode}")
        SHIPPING_ADDRESS.append("")
        SHIPPING_ADDRESS.append("Contact Information:")
        SHIPPING_ADDRESS.append(f"Email: {shipping_email}")
        if shipping_phone != "":
            SHIPPING_ADDRESS.append(f"Phone Number: {shipping_phone}")

        return redirect(url_for("payment"))
    
    return render_template("shipping.html", shipping_form=shipping_form)


## payment ##
@app.route("/payment")
@login_required
def payment():
    global EMPTY_CART, SHIPPING_ADDRESS, ORDER_DETAILS
    if EMPTY_CART == True:
        return redirect(url_for("shophome"))
    
    if SHIPPING_ADDRESS == []:
        return redirect(url_for("shipping"))
    
    return render_template("payment.html", shipping_address=SHIPPING_ADDRESS, order_details=ORDER_DETAILS)


## Create Route ##
@app.route("/config")
def get_publishable_key():
    stripe_config = {"publickey": stripe_keys["publishable_key"]}
    return jsonify(stripe_config)


## Check out session in Stripe ##
@app.route("/create-checkout-session")
def create_checkout_session():
    domain_url = "http://127.0.0.1:5002/"
    stripe.api_key = stripe_keys["secret_key"]

    try:
        # Create new Checkout Session for the order
        # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param
        checkout_session = stripe.checkout.Session.create(
            success_url=domain_url + "orderconfirmation?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=domain_url + "shipping",
            payment_method_types=["card"],
            mode="payment",
            line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': 'Order Total',
                        },
                        'unit_amount': int(ORDER_TOTAL * 100),
                    },
                    'quantity': 1,
                    }],
        )
        return jsonify({"sessionId": checkout_session["id"]})

    except Exception as e:
        return jsonify(error=str(e)), 403


## order confirmation ##
@app.route("/orderconfirmation")
@login_required
def orderconfirmation():
    global EMPTY_CART, CUSTOMER_CART, ORDER_DETAILS, ORDER_TOTAL, SHIPPING_ADDRESS
    if EMPTY_CART == True:
        return redirect(url_for("shophome"))
    
    if SHIPPING_ADDRESS == []:
        return redirect(url_for("shipping"))

    name = current_user.fullname
    order_number =  str(randint(1000, 9000)) + "-" + str(randint(100000, 200000)) + "-" + str(randint(100, 900))
    order = ""

    for line in ORDER_DETAILS:
        order += f"{line}\n"
    for line in SHIPPING_ADDRESS:
        order += f"{line}\n"

    order_confirmation_email(customer_name=name, order_number=order_number, order_details=order)
    
    # Empty user's cart after order completion
    EMPTY_CART = True
    CUSTOMER_CART = []
    ORDER_DETAILS = [" Item  ------------------------------  Price  -  Quantity "]
    SHIPPING_ADDRESS = []

    with app.app_context():
        delete_from_cart = db.session.execute(db.select(ShoppingCart).where(ShoppingCart.customer_id == current_user.id)).scalars()
        for item in delete_from_cart:
            db.session.delete(item)
            db.session.commit()

    return render_template("orderconfirmation.html", order_number=order_number)


## contact ##
@app.route("/contact", methods=["GET", "POST"])
def contact():
    contact_form = ContactForm()
    
    if contact_form.validate_on_submit():

        sender = request.form.get("full_name")
        email = request.form.get("email")
        phonenumber = request.form.get("phone")
        message = request.form.get("message")
        contact_email(sender_name=sender, sender_email=email, sender_number=phonenumber, sender_message=message)
        
        return redirect(url_for("delivered"))

    
    return render_template("contact.html", contact_form=contact_form)


## Message Delivered
@app.route("/delivered")
def delivered():
    return render_template("message_delivered.html")


## about ##
@app.route("/about")
def about():
    return render_template("about.html")


## faq ##
@app.route("/faq")
def faq():
    return render_template("faq.html")


if __name__ == "__main__":
    app.run(debug=True, port=5002)