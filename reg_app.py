from flask import Flask, render_template
import os
from dotenv import load_dotenv
from register import register_bp

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

    app.register_blueprint(register_bp)
    
    return app
    
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)