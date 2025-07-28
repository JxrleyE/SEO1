from . import shower_bp
from flask import render_template, redirect, url_for, request


@shower_bp.route('/showers')
def shower_list():
    # Shows the list of showers
    return render_template('showers/showers.html')

# 
@shower_bp.route('/showers/<int:shower_id>')
def shower_schedule(shower_id):
    # Shows the details of a specific shower
    return render_template('showers/shower_schedule.html', shower_id=shower_id)

@shower_bp.route('/showers/<int:shower_id>/book', methods=['POST'])
def book_shower(shower_id):
    # Gonna implement booking logic here
    pass