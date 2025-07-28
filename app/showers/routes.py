from . import shower_bp
from flask import render_template, redirect, url_for


@shower_bp.route('/showers')
def shower_list():
    # Display the list of showers
    return render_template('showers.html')
