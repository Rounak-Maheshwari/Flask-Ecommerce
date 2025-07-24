from app import db
from datetime import datetime


class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    date_joined = db.Column(db.DateTime(), default=datetime.utcnow)

    cart_items = db.relationship('Cart', backref='user', lazy=True)
    orders = db.relationship('Order', backref='user', lazy=True)

    def __repr__(self):
        return f'<User id: {self.id}>'


class Product(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    product_name = db.Column(db.String(100), nullable=False)
    discounted_price = db.Column(db.Float(), nullable=False)
    mrp = db.Column(db.Float(), nullable=False)
    in_stock = db.Column(db.Integer(), nullable=False)
    product_image = db.Column(db.String(1000), nullable=False)
    discount_percentage = db.Column(db.Integer(), nullable=False)
    date_added = db.Column(db.DateTime(), default=datetime.utcnow)

    carts = db.relationship('Cart', backref='product')
    orders = db.relationship('Order', backref='product')

    def __repr__(self):
        return f'<Product name: {self.product_name}>'


class Cart(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    quantity = db.Column(db.Integer(), nullable=False)

    user_link = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)
    product_link = db.Column(db.Integer(), db.ForeignKey('product.id'), nullable=False)

    def __repr__(self):
        return f'<Cart id: {self.id}>'


class Order(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    quantity = db.Column(db.Integer(), nullable=False)
    price = db.Column(db.Float(), nullable=False)
    status = db.Column(db.String(), nullable=False, default='Pending')
    payment_id = db.Column(db.String(1000), nullable=False)

    user_link = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)
    product_link = db.Column(db.Integer(), db.ForeignKey('product.id'), nullable=False)

    def __repr__(self):
        return f'<Order id: {self.id}>'



