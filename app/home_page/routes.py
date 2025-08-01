# This file is responsible for creating different routes for the home blueprint

from . import home_bp
from flask import render_template, url_for, redirect, request, flash
from flask_login import login_user, login_required, logout_user, current_user
from app.models import User, LoginForm, RegistrationForm, RegistrationForm, ChangePasswordForm, ChangeUsernameForm, SchoolSelectionForm
from app.extensions import db, bcrypt


@home_bp.route('/')
def home():
    return render_template('home.html')


# login route  - allows users to log in
@home_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():

        user = User.query.filter_by(username=form.username.data).first()

        # If user exists and password matches
        if user and bcrypt.check_password_hash(user.password,
                                              form.password.data):
            login_user(user)
            
            # Check if user has chosen a school
            if current_user.school and current_user.dorm:
                return redirect(url_for('home.dashboard'))
            else:
                return redirect(url_for('home.select_school'))
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
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        # Create new user with hashed password
        new_user = User(username=form.username.data, password=hashed_password)

        # Save to db
        db.session.add(new_user)
        db.session.commit()

        print("REGISTER PW: ", hashed_password)

        # Redirect to login page
        return redirect(url_for('home.login'))

    # Show registration page if form validation fails
    return render_template('register.html', form=form)

# School selection route - users select their school
@home_bp.route('/select-school', methods=['GET', 'POST'])
@login_required
def select_school():
    form = SchoolSelectionForm()

    # If submitted form is valid, add school to users db 
    if form.validate_on_submit():
        current_user.school = form.school.data
        current_user.dorm = form.dorm.data
        db.session.commit()
        return redirect(url_for('home.dashboard'))

    return render_template('select_school.html', form=form)  

# Dashboard route - requires user to be logged in
@home_bp.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html')


# Logout route - allows users to log out (need to be logged in)
@home_bp.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('home.login'))


# Settings route - requires user to be logged in
@home_bp.route('/settings', methods=['GET', 'POST'])
#@login_required
def settings():
    """
    Allows user to change settings (username, password), saves to database
    """
    username_form = ChangeUsernameForm()
    password_form = ChangePasswordForm()

    # Check whether username or password has been changed
    if username_form.validate_on_submit() and 'submit_username' in request.form:
        # Check if current_username matches logged-in user's username
        if username_form.current_username.data != current_user.username:
            print("ERROR: Current username does not match.")
            return render_template('settings.html', user=current_user,
                            username_form=username_form, password_form=password_form,
                            error='Incorrect Username, please try again.')
        else:
            # Check if new_username is already taken by another user
            existing_user = User.query.filter_by(username=username_form.new_username.data).first()
            if existing_user and existing_user.id != current_user.id:
                print("ERROR: New username is already taken.")
                render_template('settings.html', user=current_user,
                            username_form=username_form, password_form=password_form,
                            error='Username already taken. Please try again.')
            else:
                # Update username
                current_user.username = username_form.new_username.data
                db.session.commit()
                print("SUCCESS: Username updated successfully.")
                return redirect(url_for('home.settings'))


    # Handle password change form submission
    if password_form.validate_on_submit() and 'submit_password' in request.form:
        # Check if current_password matches logged-in user's password
        if not bcrypt.check_password_hash(current_user.password, password_form.current_password.data):
            print("ERROR: Current password does not match.")
            render_template('settings.html', user=current_user,
                            username_form=username_form, password_form=password_form,
                            error='Password does not match current password.')
        else:
            # Hash and update new password
            hashed_new_password = bcrypt.generate_password_hash(password_form.new_password.data).decode('utf-8')
            current_user.password = hashed_new_password
            db.session.commit()
            print("SUCCESS: Password updated successfully.")
            return redirect(url_for('home.settings'))


    return render_template('settings.html', user=current_user, 
                            username_form=username_form, password_form=password_form)
