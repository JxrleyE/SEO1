from . import shower_bp
from flask import render_template, redirect, url_for


@shower_bp.route('/showers')
def shower_list():
    # Logic to retrieve and display the list of showers
    return render_template('showers.html')
