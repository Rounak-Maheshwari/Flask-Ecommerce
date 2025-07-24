from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'my_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///site.db"

    db.init_app(app)
    bcrypt.init_app(app)

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html')

    from .routes.main import main
    from .routes.admin import admin
    from .routes.auth import auth

    app.register_blueprint(main)
    app.register_blueprint(admin)
    app.register_blueprint(auth)

    return app

