# This file is for importing and initializing Flask extensions
# These extensions will are used db management,
# user authentication, and password hashing

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()
