# This file is responsible for creating and managing the User model and forms
# for registration/login
from .extensions import db
from flask_login import UserMixin
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError


# Define the User model
# This will be used to store user information in the database
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)


# Form for user registration with validation
class RegistrationForm(FlaskForm):
    username = StringField(
        validators=[InputRequired(), Length(min=2, max=20)],
        render_kw={"placeholder": "Username"}
    )
    password = PasswordField(
        validators=[InputRequired(), Length(min=6, max=20)],
        render_kw={"placeholder": "Password"}
    )
    submit = SubmitField('Register')

    # Check if the username already exists
    def validate_username(self, username):
        existing_user = User.query.filter_by(username=username.data).first()
        if existing_user:
            raise ValidationError('Username already exists!')


# Form for user login with validation
class LoginForm(FlaskForm):
    username = StringField(
        validators=[InputRequired(), Length(min=2, max=20)],
        render_kw={"placeholder": "Username"}
    )
    password = PasswordField(
        validators=[InputRequired(), Length(min=6, max=20)],
        render_kw={"placeholder": "Password"}
    )
    submit = SubmitField('Login')
