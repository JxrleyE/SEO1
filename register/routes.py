from flask import request
from . import register_bp
from flask import Flask, render_template

@register_bp.route('/')
def register():
    return render_template('home.html')