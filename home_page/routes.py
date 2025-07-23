from . import home_bp
from flask import render_template, url_for, redirect
from flask_login import login_user, login_required, logout_user
from models import User, LoginForm, RegistrationForm
from extensions import db, bcrypt

@home_bp.route('/')
def home():
    return render_template('home.html')

@home_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        #checks if user is registered 
        user = User.query.filter_by(username=form.username.data).first()

        # If user exists and password matches
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('home.dashboard'))
        else:
            # Show error for wrong username or password
            return render_template('login.html', form=form, error='Invalid username or password')
        
    return render_template('login.html', form=form)

@home_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('home.login'))
    
    # form is invalid load the registration page up again
    return render_template('register.html', form=form)

@home_bp.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html')

@home_bp.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('home.login'))