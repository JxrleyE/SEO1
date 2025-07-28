from . import shower_bp
from flask import render_template, redirect, url_for, request
from datetime import datetime, timedelta

# Show the list of showers
@shower_bp.route('/showers')
def shower_list():
    return render_template('showers/showers.html')

# Show the schedule for a specific shower
@shower_bp.route('/showers/<int:shower_id>')
def shower_schedule(shower_id):
    
    # Need to make all the possible times for booking | displays in regular 12-hour format
    early_morning = []
    morning = []
    afternoon = []
    evening = []
    for hour in range(24):
        for minute in [0, 30]:
             time_obj = datetime.strptime(f"{hour:02}:{minute:02}", "%H:%M")
             
             # We have to store the time differently for db vs display

             db_time = time_obj.time()  # Use military time for db
             
             # Display time (1:00 PM - 1:30 PM)
             start_time = time_obj.strftime("%I:%M %p")
             end_time = (time_obj + timedelta(minutes=30)).strftime("%I:%M %p")
             
             # Dictionary to hold both formats
             time_slot = {
                 # 'db_time': start_time_db,  # For storing in database
                 'display_time': f"{start_time} - {end_time}"  # For showing user
             }

            # Times are determined by the hour
             if hour < 6:
                 early_morning.append(time_slot)
             elif hour < 12:
                 morning.append(time_slot)
             elif hour < 18:
                 afternoon.append(time_slot)
             else:
                 evening.append(time_slot)

    # Shows the details of a specific shower and pass in the time slots
    return render_template('showers/shower_schedule.html', shower_id=shower_id,
                           early_morning=early_morning, morning=morning, afternoon=afternoon,
                             evening=evening)

@shower_bp.route('/showers/<int:shower_id>/book', methods=['POST'])
def book_shower(shower_id):
    # Gonna implement booking logic here
    pass