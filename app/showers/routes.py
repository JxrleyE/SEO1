from . import shower_bp
from flask import render_template, redirect, url_for, request
from datetime import datetime


@shower_bp.route('/showers')
def shower_list():
    # Shows the list of showers
    return render_template('showers/showers.html')

# 
@shower_bp.route('/showers/<int:shower_id>')
def shower_schedule(shower_id):

    # Need to make all the possible times for booking | displays in regular 12-hour format
    times = []
    for hour in range(24):
        for minute in [0, 30]:
             time_obj = datetime.strptime(f"{hour:02}:{minute:02}", "%H:%M")
             time_str = time_obj.strftime("%I:%M %p")
             times.append(time_str)

    # Shows the details of a specific shower and pass in the time slots
    return render_template('showers/shower_schedule.html', shower_id=shower_id, 
                           times=times)

@shower_bp.route('/showers/<int:shower_id>/book', methods=['POST'])
def book_shower(shower_id):
    # Gonna implement booking logic here
    pass