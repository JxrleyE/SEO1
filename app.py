from flask import Flask
import os
from dotenv import load_dotenv

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

    # local import for simplicity and readability
    from sms_messaging import sms_bp
    
    # test route
    @app.route('/')
    def home():
        return "<h1>Testing!</h1>"

    # register blueprint for /sms route
    app.register_blueprint(sms_bp)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=3000)
