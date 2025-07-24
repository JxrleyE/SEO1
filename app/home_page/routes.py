# This file is responsible for creating different routes for the home blueprint

from . import home_bp
from flask import render_template, url_for, redirect
from flask_login import login_user, login_required, logout_user
from app.models import User, LoginForm, RegistrationForm
from app.extensions import db, bcrypt


@home_bp.route('/')
def home():
    return render_template('home.html')


# login route  - allows users to log in
@home_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        # Check if user exists in database
        user = User.query.filter_by(username=form.username.data).first()

        # If user exists and password matches
        if user and bcrypt.check_password_hash(user.password,
                                               form.password.data):
            login_user(user)
            return redirect(url_for('home.dashboard'))
        else:
            # Show error msg for wrong username or password
            return render_template('login.html', form=form,
                                   error='Invalid username or password')

    # Show login form again if failed form
    return render_template('login.html', form=form)


# Registration route - allows new users to register
@home_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        # Hash password before storing in db
        hashed_password = bcrypt.generate_password_hash(form.password.data)

        # Create new user with hashed password
        new_user = User(username=form.username.data, password=hashed_password)

        # Save to db
        db.session.add(new_user)
        db.session.commit()

        # Redirect to login page
        return redirect(url_for('home.login'))

    # Show registration page if failed up form
    return render_template('register.html', form=form)


# Dashboard route - requires user to be logged in
@home_bp.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    """Protected dashboard route - requires authentication"""
    return render_template('dashboard.html')


# Logout route - allows users to log out (need to be logged in)
@home_bp.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('home.login'))
