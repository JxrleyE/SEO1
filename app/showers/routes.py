from . import shower_bp
from flask import render_template, redirect, url_for, request


@shower_bp.route('/showers')
def shower_list():
    # Shows the list of showers
    return render_template('showers/showers.html')

# 
@shower_bp.route('/showers/<int:shower_id>')
def shower_schedule(shower_id):

    # Need to make all the possible times for booking
    times = []
    for hour in range(24):
        for minute in [0, 30]:
            time_str = f"{hour:02}:{minute:02}"
            times.append(time_str)

    # Shows the details of a specific shower and pass in the time slots
    return render_template('showers/shower_schedule.html', shower_id=shower_id, 
                           times = times)

@shower_bp.route('/showers/<int:shower_id>/book', methods=['POST'])
def book_shower(shower_id):
    # Gonna implement booking logic here
    pass