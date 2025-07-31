from . import shower_bp, forms
from flask import render_template, redirect, url_for, request, flash, session
from datetime import datetime, timedelta
from app_queue.services import add_to_queue, shower_available

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
             
             # We have to store the time differently for db vs. display

             db_time = time_obj.time()  # Use military time for db
             
             # Display time (1:00 PM - 1:30 PM)
             start_time = time_obj.strftime("%I:%M %p")
             end_time = (time_obj + timedelta(minutes=30)).strftime("%I:%M %p")
             
             # Dictionary to hold both formats
             time_slot_dict = {
                 'db_value': db_time,  
                 'display_value': f"{start_time} - {end_time}",  
                 'available': shower_available(shower_id, db_time)
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
    return render_template('showers/shower_schedule.html', shower_id=shower_id,
                           early_morning=early_morning, morning=morning, afternoon=afternoon,
                             evening=evening)


@shower_bp.route('/showers/<int:shower_id>/book', methods=['GET', 'POST'])
def book_shower(shower_id):
    form = forms.EventRegistrationForm()
    if request.method == 'POST' and 'time_slot' in request.form:
        # Get time slot to put into db
        time_slot = request.form.get('time_slot')
        time_slot_display = request.form.get('time_slot_display')
        print(f'TIME SLOT: {time_slot}')
        print(f'TIME SLOT DISPLAY {time_slot_display}')
        
        session['booking'] = {
            'shower_id': shower_id,
            'time_slot': time_slot,
            'time_slot_display': time_slot_display
        }
    

    if form.validate_on_submit():
        # Retrieve data from POST request
        booking_data = session.get('booking')

        time_slot = booking_data['time_slot']
        time_slot_display = booking_data['time_slot_display']
        phone_number = form.phone_number.data
        event = 'shower'
        duration = 30

        # Place info into db
        try:
            print("Calling adding to queue", phone_number, event, shower_id, time_slot, duration)
            add_to_queue(phone_number, event, shower_id, time_slot, duration)
            print("Added to queue successfully!")
            # services.send_confirmation_message(phone_number, event, registration_time_utc, duration)
            flash(f'You have successfully registered to {event} at {time_slot_display}!', 'success')
            return redirect(url_for('home.dashboard'))
        except Exception as e:
            return render_template("showers/register_event.html", form=form, error=e, shower_id=shower_id)
            print(e)

    return render_template("showers/register_event.html", form=form, shower_id=shower_id)
