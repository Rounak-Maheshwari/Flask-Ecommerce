from werkzeug.utils import secure_filename
from flask import Blueprint, render_template, url_for, session, redirect, request, flash, send_from_directory
from app.models.models import Product, User, Order
from app import db

admin = Blueprint('admin', __name__)


@admin.route('/media/<path:filename>')
def get_image(filename):
    return send_from_directory('../media', filename)


@admin.route('/add-product', methods=['GET', 'POST'])
def add_product():
    if session['user_id'] == 1:
        if request.method == 'POST':
            product_name = request.form.get('product-name')
            mrp = float(request.form.get('mrp'))
            discount_price = float(request.form.get('discount-price'))
            discount_percent = int(request.form.get('discount-percent'))
            in_stock = int(request.form.get('in-stock-amt'))

            file = request.files.get('product-image')
            file_name = secure_filename(file.filename)

            file_path = f'./media/{file_name}'
            file.save(file_path)

            new_product = Product(product_name=product_name, discounted_price=discount_price, mrp=mrp, in_stock=in_stock,
                                  product_image=file_path, discount_percentage=discount_percent)
            db.session.add(new_product)
            db.session.commit()
            flash(f'{product_name} added!', 'success')
        return render_template('add-product.html')

    return render_template('404.html')


@admin.route('/shop-products', methods=['GET', 'POST'])
def shop_products():
    if session['user_id'] == 1:
        products = Product.query.order_by('date_added').all()
        return render_template('shop-products.html', products=products)

    return render_template('404.html')


@admin.route('/update-product/<int:product_id>', methods=['GET', 'POST'])
def update_product(product_id):
    if session['user_id'] == 1:
        product = Product.query.filter_by(id=product_id).first()
        if product:
            if request.method == 'POST':
                product_name = request.form.get('product-name')
                mrp = float(request.form.get('mrp'))
                discount_price = float(request.form.get('discount-price'))
                discount_percent = int(request.form.get('discount-percent'))
                in_stock = int(request.form.get('in-stock-amt'))

                file = request.files.get('product-image')
                file_name = secure_filename(file.filename)

                file_path = f'./media/{file_name}'
                file.save(file_path)

                try:
                    product.product_name = product_name
                    product.mrp = mrp
                    product.discounted_price = discount_price
                    product.discount_percentage = discount_percent
                    product.in_stock = in_stock
                    product.product_image = file_path

                    db.session.commit()
                    flash(f'{product_name} updated successfully', 'success')
                    return redirect(url_for('admin.shop-products'))

                except Exception as ex:
                    flash(f'Item not updated', 'danger')

            return render_template('update-product.html', product=product)

    return render_template('404.html')


@admin.route('/delete-product/<int:product_id>', methods=['GET', 'POST'])
def delete_product(product_id):
    if session['user_id'] == 1:
        product = Product.query.filter_by(id=product_id).first()
        db.session.delete(product)
        db.session.commit()
        flash(f'{product.product_name} deleted', 'success')
        return redirect(url_for('admin.shop-products'))

    return render_template('404.html')


@admin.route('/app-users')
def app_users():
    if session['user_id'] == 1:
        users = User.query.order_by('date_joined')
        return render_template('users.html', users=users)
    return render_template('404.html')


@admin.route('/admin-panel')
def admin_panel():
    if session['user_id'] == 1:
        return render_template('admin.html')
    return render_template('404.html')


@admin.route('/view-orders')
def view_orders():
    if session['user_id'] == 1:
        orders = Order.query.all()
        return render_template('view-orders.html', orders=orders)

    return render_template('404.html')


@admin.route('/update-status/<int:order_id>', methods=['GET', 'POST'])
def update_status(order_id):
    if session['user_id'] == 1:
        order = Order.query.filter_by(id=order_id).first()
        if request.method == 'POST':
            status = request.form.get('status')
            order.status = status
            db.session.commit()
            flash('Order Status Updated.', 'success')
            return redirect(url_for('admin.view_orders'))
        return render_template('update-order-status.html', order=order)

    return render_template('404.html')