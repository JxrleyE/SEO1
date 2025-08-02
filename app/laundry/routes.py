from . import laundry_bp
from flask import render_template, redirect, url_for, request, flash, session
from datetime import datetime, timedelta
from app_queue.services import add_to_queue, shower_available
from sms_messaging import services
from app.showers.forms import EventRegistrationForm
import pytz

# Show the list of laundry machines
@laundry_bp.route('/laundry')
def laundry_list():
    return render_template('laundry/machines.html')

# Show the schedule for a specific shower
@laundry_bp.route('/washer/<int:washer_id>')
def washer_schedule(washer_id):
    # Need to make all the possible times for booking | displays in regular 12-hour format
    early_morning = []
    morning = []
    afternoon = []
    evening = []
    for hour in range(24):
        for minute in [0, 30]:
             time_obj = datetime.strptime(f"{hour:02}:{minute:02}", "%H:%M")
             
             # We have to store the time differently for db vs. display

             db_time = time_obj.strftime("%H:%M")  # Use military time for db
             
             # Display time (1:00 PM - 1:30 PM)
             start_time = time_obj.strftime("%I:%M %p")
             end_time = (time_obj + timedelta(minutes=30)).strftime("%I:%M %p")
             
             # Dictionary to hold both formats
             time_slot_dict = {
                 'db_value': db_time,  
                 'display_value': f"{start_time} - {end_time}",  
                 'available': washer_available(washer_id, db_time)
             }

            # Times are determined by the hour
             if hour < 6:
                 early_morning.append(time_slot_dict)
             elif hour < 12:
                 morning.append(time_slot_dict)
             elif hour < 18:
                 afternoon.append(time_slot_dict)
             else:
                 evening.append(time_slot_dict)

    # Shows the details of a specific shower and pass in the time slots
    return render_template('laundry/washer_schedule.html', washer_id=washer_id,
                           early_morning=early_morning, morning=morning, afternoon=afternoon,
                             evening=evening)

