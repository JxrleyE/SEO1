# This file is for running the Flask application
from flask import Flask
import os
from dotenv import load_dotenv
from .extensions import db, login_manager, bcrypt, migrate
from .models import User


# Load environment variables from .env
load_dotenv()


# Get .env variables
SECRET_KEY = os.environ.get("SECRET_KEY")
SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI", "sqlite:///database.db")


def create_app():
    '''
    Create Flask app
    '''
    app = Flask(__name__)

    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI


    # Initialize entensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'home.login'
    migrate.init_app(app, db)


    # Loads user for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))


    # Initialize password hashing extension
    bcrypt.init_app(app)


    # Register blueprint for home page routes
    from .home_page import home_bp
    app.register_blueprint(home_bp)

    # Register blueprint for showers routes
    from .showers import shower_bp
    app.register_blueprint(shower_bp)

    # Register blueprint for /sms route
    from sms_messaging import sms_bp
    app.register_blueprint(sms_bp)


    return app
