"""Hi Audience"""
from pymongo.errors import DuplicateKeyError
from flask_login import LoginManager, login_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from flask import Flask, render_template, request, redirect, url_for, flash
import uuid

from db import get_user, save_user, remove_from_cart, add_into_cart, set_qty
from db import user_cart_prod, add_info, get_cart
from db import all_products, get_product, get_product_id, all_updates
from db import bill, mail, prod_qty, get_total, prod_id, search_prod
from db import all_prod, update_product, save_product, latest_prod
from db import all_orders, ord_track, track_all, empty_cart, total_items

app = Flask(__name__)
app.secret_key = "granthbagadiagranthbagadia"
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)


tags = ['PS4', 'PS5', 'XBOX X', 'XBOX-1', 'SURFACE', 'ACCESSORIES', 'NINTENDO']


class New(FlaskForm):
    """Hi Audience"""
    name = StringField('name')
    category = StringField('category')
    image = StringField('image')
    info = StringField('info')
    mrp = IntegerField('MRP')
    srp = IntegerField('SRP')
    quantity = IntegerField('Quantity')
    submit = SubmitField('Submit')


class Info(FlaskForm):
    """Hi Audience"""
    name = StringField('Name')
    email = StringField('E-Mail')
    phone = StringField('Phone')
    address = StringField('Address')
    submit = SubmitField('Submit')


class Track(FlaskForm):
    """Hi Audience"""
    idt = StringField('Order ID')
    status = StringField('Tracking Service')
    submit = SubmitField('Tracking ID')


class Update(FlaskForm):
    """Hi Audience"""
    idt = StringField('idt')
    mrp = IntegerField('MRP')
    srp = IntegerField('SRP')
    quantity = IntegerField('quantity')
    submit = SubmitField('Submit')


class Contact(FlaskForm):
    """Hi Audience"""
    mail = StringField('Email - ID')
    message = StringField('Message')


class TrackOrder(FlaskForm):
    """Hi Audience"""
    order_id = StringField('Order ID')


@app.context_processor
def base():
    """Hi Audience"""
    if current_user.is_authenticated:
        tqty = total_items(current_user.email)
    else:
        tqty = 0
    return dict(total_qty=tqty)


@app.route("/")
@app.route("/home", methods=['GET', 'POST'])
def home():
    """Hi Audience"""
    if current_user.is_authenticated:
        latest_products = latest_prod(current_user.email)
    else:
        latest_products = latest_prod()
    latest_products.reverse()
    updates = all_updates()
    updates.reverse()
    return render_template('home.html', latest_prod=latest_products, updates=updates)


@app.route("/contact", methods=['GET', 'POST'])
def contact():
    """Hi Audience"""
    form = Contact()
    if form.validate_on_submit:
        message = f"""
    From: {form.mail.data}
    Message: {form.message.data}
    """
        mail("granthbagadia2004@gmail.com", message)
        flash("Query Sent Successfully")
        return render_template('contact us.html')


@app.route("/cart", methods=['GET', 'POST'])
def cart():
    """Hi Audience"""
    if current_user.is_authenticated:
        current = current_user.email
        tamount = get_total(current)
        tqty = total_items(current)
        temp_cart = get_cart(current_user.email)
        temp_x = []
        for i in temp_cart:
            temp_ut = get_product_id(i['_id'])
            temp_ut['cqty'] = i['cqty']
            temp_ut['total'] = i['cqty']*temp_ut['srp']
            temp_x.append(temp_ut)
            if request.method == "POST":
                name = request.form.get("name")
                phone = request.form.get("phone")
                email = request.form.get("email")
                address = request.form.get("address")
        return render_template('cart.html', current=current, cart=temp_x,
            total_amount=tamount, total_qty=tqty)
    return redirect(url_for('home'))


@app.route("/<temp_x>", methods=['GET', 'POST'])
def products(temp_x):
    """Hi Audience"""
    if temp_x in tags:
        temp_products = list(all_products(temp_x))
        for i in temp_products:
            for j in i:
                if current_user.is_authenticated:
                    tag = j.get("_id")
                    cqty = user_cart_prod(
                        current_user.email, str(get_product(tag)['_id']))
                    j['cqty'] = cqty
                else:
                    j['cqty'] = 0
        cartx = []
        if current_user.is_authenticated:
            current = current_user.email
            temp_cart = get_cart(current_user.email)
            for i in temp_cart:
                temp_ut = get_product_id(i['_id'])
                temp_ut['cqty'] = i['cqty']
                cartx.append(temp_ut)
        return render_template('products.html', lenproducts=len(temp_products),
            products=temp_products, cart=cartx, x=temp_x)
    return render_template('505.html')


@app.route("/product/<temp_x>", methods=['GET', 'POST'])
def product(temp_x):
    if temp_x in prod_id():
        if current_user.is_authenticated:
            cqty = user_cart_prod(current_user.email, temp_x)
        else:
            cqty = 1
        return render_template('item.html', product=get_product(temp_x), cqty=cqty)
    return render_template('505.html')


@app.route("/add/<temp_x>", methods=['GET', 'POST'])
def add(temp_x):
    """Hi Audience"""
    if current_user.is_authenticated:
        add_into_cart(current_user.email, temp_x)
        # update_cart(current_user.email, temp_x)
        flash("Item Added Successfully")
        return redirect(url_for('cart'))
    user_id = str(uuid.uuid1())
    try:
        save_user(user_id)
        user = get_user(user_id)
        login_user(user)
        return redirect(url_for('add', temp_x=temp_x))
    except DuplicateKeyError:
        user = get_user(user_id)
        login_user(user)
        return redirect(url_for('add', temp_x=temp_x))


@app.route("/remove/<temp_x>", methods=['GET', 'POST'])
def remove(temp_x):
    """Hi Audience"""
    if current_user.is_authenticated:
        remove_from_cart(current_user.email, temp_x)
        # update_cart(current_user.email, temp_x)
        flash("Item Added Successfully")
        return redirect(url_for('cart'))
    user_id = str(uuid.uuid1())
    try:
        save_user(user_id)
        user = get_user(user_id)
        login_user(user)
        return redirect(url_for('add', temp_x=temp_x))
    except DuplicateKeyError:
        user = get_user(user_id)
        login_user(user)
        return redirect(url_for('add', temp_x=temp_x))


@app.route("/pay", methods=['GET', 'POST'])
def pay():
    """Hi Audience"""
    form = Info()
    if form.validate_on_submit:
        email = form.email.data
        name = form.name.data
        phone = form.phone.data
        address = form.address.data
        add_info(current_user.email, email, name, phone, address)
    return render_template('pay.html', email=email)


@app.route("/success", methods=['GET', 'POST'])
def success():
    """Hi Audience"""
    email = current_user.email
    idt, mail_to = bill(email)
    empty_cart(email)
    mail("granthbagadia2004@gmail.com", "Test Mail")
    message = f"""From: From granthbagadia2004@gmail.com
    Subject: Order Placed Successfully!

    This is a confirmation for your order on Games-Trade India.
    Your Order ID is {str(idt)}
    """
    mail(mail_to, message)
    prod_qty(idt)
    flash("Order Placed Successfully!")
    return redirect(url_for('home'))


@app.route("/home-admin", methods=['GET', 'POST'])
def home_admin():
    """Hi Audience"""
    return render_template('home2.html')


@app.route("/new_product", methods=['GET', 'POST'])
def new_product():
    """Hi Audience"""
    form = New()
    return render_template('new_product.html', products=all_prod(),
        form=form, message="Hello There")


@app.route("/new_prod", methods=['GET', 'POST'])
def new_prod():
    """Hi Audience"""
    form = New()
    if form.validate_on_submit:
        category = form.category.data
        name = form.name.data
        mrp = form.mrp.data
        srp = form.srp.data
        temp_info = form.info.data
        image = form.image.data
        if (category or name or mrp or srp or image or temp_info) == "":
            message = "Invalid Details"
        else:
            message = save_product(
                category, name, quantity, mrp, srp, image, temp_info)
        return render_template('new_product.html', products=all_prod(), form=form, message=message)
    return render_template('new_product.html', products=all_prod(),
        form=form, message="Hello There")


@app.route("/update_prod", methods=['GET', 'POST'])
def update_prod():
    """Hi Audience"""
    form = Update()
    try:
        idt = form.idt.data
        mrp = form.mrp.data
        srp = form.srp.data
        quantity = form.quantity.data
        update_product(idt, mrp, srp, quantity)
        return render_template('update_product.html', products=all_prod(), form=form)
    except TypeError:
        return render_template('update_product.html', products=all_prod(), form=form)


@app.route("/add_track", methods=['GET', 'POST'])
def add_track():
    """Hi Audience"""
    form = Track()
    try:
        idt = form.idt.data
        temp_status = form.status.data
        ord_track(idt, temp_status)
    except TypeError:
        pass
    return render_template('new_ord.html', orders=all_orders(), form=form, products=all_prod())


@app.route("/delivered/<order_id>", methods=['GET', 'POST'])
def delivered(order_id):
    """Hi Audience"""
    ord_track(order_id, 'Delivered')
    return redirect(url_for('add_track'))


@app.route("/check_order", methods=['GET', 'POST'])
def check_order():
    """Hi Audience"""
    return render_template('check_order.html', orders=track_all(), products=all_prod())


@app.route("/track-order", methods=['GET', 'POST'])
def track_order():
    """Hi Audience"""
    form = TrackOrder()
    if form.validate_on_submit:
        order_id = form.order_id.data
        for i in all_orders():
            if i['_id'] == order_id:
                return render_template('track_order.html', order=i, products=all_prod(), stat=1)
        for i in all_orders():
            if i['_id'] == order_id:
                return render_template('track_order.html', order=i, products=all_prod(), stat=1)
    return render_template('track_order.html', stat=0)


@login_manager.user_loader
def load_user(email):
    """Hi Audience"""
    return get_user(email)


if __name__ == '__main__':
    app.run(debug=True, port=3000)
