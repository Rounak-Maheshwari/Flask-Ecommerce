from flask import Blueprint, render_template, session, redirect, url_for, flash, request
from app.models.models import User, Product, Cart, Order
from app import db

main = Blueprint('main', __name__)


@main.route('/')
def home():
    if 'user_id' not in session:
        flash('You need to be logged in.', 'danger')
        return redirect(url_for('auth.login'))
    user = User.query.filter_by(id=session['user_id']).first()
    products = Product.query.all()
    return render_template('home.html', user=user, products=products,
                           cart=Cart.query.filter_by(user_link=session['user_id']).all())


@main.route('/cart')
def view_cart():
    if 'user_id' not in session:
        flash('You need to be logged in.', 'danger')
        return redirect(url_for('auth.login'))
    cart = Cart.query.filter_by(user_link=session['user_id']).all()
    total_amount = 0
    for item in cart:
        amount = item.product.discounted_price * item.quantity
        total_amount += amount

    return render_template("cart.html", cart=cart, total_amount=total_amount)


@main.route('/add-to-cart/<int:product_id>', methods=['GET', 'POST'])
def add_to_cart(product_id):
    if 'user_id' not in session:
        flash('You need to be logged in.', 'danger')
        return redirect(url_for('auth.login'))

    cart_exists = Cart.query.filter_by(product_link=product_id, user_link=session['user_id']).first()
    if cart_exists:
        cart_exists.quantity += 1
        db.session.commit()
        flash('Item incremented successfully', 'success')
    else:
        cart = Cart(quantity=1, user_link=session['user_id'], product_link=product_id)
        db.session.add(cart)
        db.session.commit()
        flash('Item added to cart', 'success')
    return redirect(url_for('main.view_cart'))


@main.route('/remove-cart-product/<int:cart_id>', methods=['POST'])
def remove_cart_product(cart_id):
    if 'user_id' not in session:
        flash('You need to be logged in.', 'danger')
        return redirect(url_for('auth.login'))

    cart = Cart.query.filter_by(id=cart_id).first()
    db.session.delete(cart)
    db.session.commit()
    flash('Item removed from the cart.')
    return redirect(url_for('main.view_cart'))


@main.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if 'user_id' not in session:
        flash('You need to be logged in.', 'danger')
        return redirect(url_for('auth.login'))

    user = User.query.filter_by(id=session['user_id']).first()
    cart = Cart.query.filter_by(user_link=user.id).all()

    if request.method == 'POST':
        first_name = request.form.get('first-name')
        last_name = request.form.get('last-name')
        address = request.form.get('address')
        city = request.form.get('city')
        state = request.form.get('state')
        pin_code = request.form.get('pin')
        phone = request.form.get('phone')

    total_amount = 0
    for item in cart:
        amount = item.product.discounted_price * item.quantity
        total_amount += amount

    return render_template('checkout.html', user=user, cart=cart, total_amount=total_amount)


@main.route('/order_confirmed')
def order_confirm():
    if 'user_id' not in session:
        flash('You need to be logged in.', 'danger')
        return redirect(url_for('auth.login'))
    else:
        cart = Cart.query.filter_by(user_link=session['user_id']).all()
        if len(cart) < 1:
            flash('Your cart is empty.', 'danger')
        else:
            for item in cart:
                product = Product.query.get(item.product_link)
                new_order = Order(quantity=item.quantity, user_link=session['user_id'], product_link=product.id,
                                  price=item.quantity * product.discounted_price, payment_id=1)
                db.session.add(new_order)
                db.session.delete(item)
            db.session.commit()

            flash('Your order has been placed', 'success')
    return redirect(url_for('main.orders'))


@main.route('/orders')
def orders():
    if 'user_id' not in session:
        flash('You need to be logged in.', 'danger')
        return redirect(url_for('auth.login'))

    all_orders = Order.query.filter_by(user_link=session['user_id']).all()
    return render_template('orders.html', orders=all_orders)


@main.route('/search', methods=['GET', 'POST'])
def search():
    if 'user_id' not in session:
        flash('You need to be logged in.', 'danger')
        return redirect(url_for('auth.login'))
    elif request.method == 'POST':
        search_product = request.form.get('search-product')
        products = Product.query.filter(Product.product_name.ilike(f'%{search_product}%')).all()
        return render_template('search.html', products=products,
                               cart=Cart.query.filter_by(user_link=session['user_id']).all())

    return render_template('search.html')


@main.route('/contact-us', methods=['GET', 'POST'])
def contact_us():
    if 'user_id' not in session:
        flash('You need to be logged in.', 'danger')
        return redirect(url_for('auth.login'))
    if request.method == 'POST':
        flash('Your message has been sent. Thank you', 'success')
    return render_template('contact.html')


@main.route('/about-us')
def about_us():
    if 'user_id' not in session:
        flash('You need to be logged in.', 'danger')
        return redirect(url_for('auth.login'))
    return render_template('about.html')



