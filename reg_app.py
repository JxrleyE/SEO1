from flask import Flask, render_template
import os
from dotenv import load_dotenv
from home_page import home_bp
from database import db

# load environment variable from .env
load_dotenv()

# .env variables
SECRET_KEY = os.environ.get("SECRET_KEY")


def create_app():
    '''
    Creates entryway that serves all content
    '''
    app = Flask(__name__)
    app.config['SECRET_KEY'] = SECRET_KEY

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

    # Initialize database
    db.init_app(app)

    app.register_blueprint(home_bp)
    
    return app
    
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)