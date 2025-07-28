from . import shower_bp
from flask import render_template, redirect, url_for, request
from datetime import datetime


@shower_bp.route('/showers')
def shower_list():
    # Show the list of showers
    return render_template('showers/showers.html')

# 
@shower_bp.route('/showers/<int:shower_id>')
def shower_schedule(shower_id):

    # Validate shower_id is only between 1-4
    if shower_id < 1 or shower_id > 4:
        return redirect(url_for('showers.shower_list'))
    
    # Need to make all the possible times for booking | displays in regular 12-hour format
    morning = []
    afternoon = []
    evening = []
    for hour in range(24):
        for minute in [0, 30]:
             time_obj = datetime.strptime(f"{hour:02}:{minute:02}", "%H:%M")
             time_str = time_obj.strftime("%I:%M %p")
             
             if hour < 12:
                 morning.append(time_str)
             elif hour < 18:
                 afternoon.append(time_str)
             else:
                 evening.append(time_str)

    # Shows the details of a specific shower and pass in the time slots
    return render_template('showers/shower_schedule.html', shower_id=shower_id, 
                           morning=morning, afternoon=afternoon, evening=evening)

@shower_bp.route('/showers/<int:shower_id>/book', methods=['POST'])
def book_shower(shower_id):
    # Gonna implement booking logic here
    pass