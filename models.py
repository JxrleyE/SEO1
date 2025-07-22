from extend_db import db
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

# Define the User model
# This will be used to store user information in the database
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    phone_number = db.Column(db.String(10), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)