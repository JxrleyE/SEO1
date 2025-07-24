# This file is for running the Flask application
from flask import Flask
import os
from dotenv import load_dotenv
from .home_page import home_bp
from .extensions import db, login_manager, bcrypt
from .models import User

# Load environment variables from .env
load_dotenv()

# Get secret key from environment variables
SECRET_KEY = os.environ.get("SECRET_KEY")


def create_app():
    # Create Flask app
    app = Flask(__name__)

    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

    # Initialize database
    db.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = 'home.login'

    # Loads user for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Initialize password hashing extension
    bcrypt.init_app(app)

    # Register blueprint for home page routes
    app.register_blueprint(home_bp)

    return app
