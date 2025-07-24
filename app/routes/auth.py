from flask import Blueprint, render_template, redirect, url_for, session, request, flash
from app import bcrypt, db
from app.models.models import User

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            session['user_id'] = user.id
            flash("Logged In", 'success')
            return redirect(url_for('main.home'))
        elif not user:
            flash("Email does not exist", 'success')
            return redirect(url_for('auth.register'))
        else:
            flash('Password is incorrect', 'success')
    return render_template('login.html')


@auth.route('/sign-up', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm-password')

        user = User.query.filter_by(email=email).first()

        if user:
            flash('Email already exists. Try with different email', 'danger')
        else:
            if password == confirm_password:
                hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
                new_user = User(username=username, email=email, password=hashed_password)
                db.session.add(new_user)
                db.session.commit()
                flash('Account Successfully Created', 'success')
                return redirect(url_for('auth.login'))
            else:
                flash('Password does not match', 'danger')

    return render_template('register.html')


@auth.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Logged out', 'success')

    return redirect(url_for('auth.login'))


@auth.route('/profile/<int:user_id>')
def profile(user_id):
    if 'user_id' not in session:
        flash('You need to be logged in.', 'danger')
        return redirect(url_for('auth.login'))
    user = User.query.filter_by(id=session['user_id']).first()
    return render_template('profile.html', user=user)


@auth.route('/change-password', methods=['POST'])
def change_password():
    if 'user_id' not in session:
        flash('You need to be logged in.', 'danger')
        return redirect(url_for('auth.login'))
    user = User.query.filter_by(id=session['user_id']).first()
    if user:
        current_password = request.form.get('old-password')
        new_password = request.form.get('new-password')
        confirm_new_password = request.form.get('confirm-new-password')

        if new_password != confirm_new_password:
            flash('The passwords doesnot match!', 'danger')
        elif bcrypt.check_password_hash(user.password, current_password) and new_password == confirm_new_password:
            new_hashed_password = bcrypt.generate_password_hash(password=new_password)
            user.password = new_hashed_password
            db.session.commit()
            flash('Your password has been updated!', 'success')
    return redirect(url_for('auth.profile', user_id=user.id))
