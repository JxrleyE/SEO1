from flask import Flask
import os
from dotenv import load_dotenv
from home_page import home_bp
from extensions import db, login_manager, bcrypt
from models import User

# load environment variable from .env
load_dotenv()

# .env variables
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

    # User loader for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Initialize bcrypt 
    bcrypt.init_app(app)

    app.register_blueprint(home_bp)
    
    return app
    
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)