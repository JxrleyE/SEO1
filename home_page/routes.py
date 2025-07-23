from flask import request
from . import home_bp
from flask import Flask, render_template, url_for, redirect
from models import User, LoginForm, RegistrationForm
from extensions import db
from extend_bcrypt import bcrypt

@home_bp.route('/')
def home():
    return render_template('home.html')

@home_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
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
    
    return render_template('register.html', form=form)