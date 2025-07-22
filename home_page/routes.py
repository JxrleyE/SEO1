from flask import request
from . import home_bp
from flask import Flask, render_template, url_for
from models import User

@home_bp.route('/')
def home():
    return render_template('home.html')

@home_bp.route('/login')
def login():
    return render_template('login.html')

@home_bp.route('/register')
def register():
    return render_template('register.html')