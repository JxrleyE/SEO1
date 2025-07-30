from . import shower_bp, forms
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
             
             # We have to store the time differently for db vs. display

             db_time = time_obj.time()  # Use military time for db
             
             # Display time (1:00 PM - 1:30 PM)
             start_time = time_obj.strftime("%I:%M %p")
             end_time = (time_obj + timedelta(minutes=30)).strftime("%I:%M %p")
             
             # Dictionary to hold both formats
             time_slot = {
                 'db_time': db_time,  
                 'display_time': f"{start_time} - {end_time}"  
             }

            # Times are determined by the hour
             if hour < 6:
                 early_morning.append(time_slot['display_time'])
             elif hour < 12:
                 morning.append(time_slot['display_time'])
             elif hour < 18:
                 afternoon.append(time_slot['display_time'])
             else:
                 evening.append(time_slot['display_time'])

    # Shows the details of a specific shower and pass in the time slots
    return render_template('showers/shower_schedule.html', shower_id=shower_id,
                           early_morning=early_morning, morning=morning, afternoon=afternoon,
                             evening=evening)


@shower_bp.route('/showers/<int:shower_id>/book', methods=['POST'])
def book_shower(shower_id):
    # Gonna implement booking logic here
    form = forms.EventRegistrationForm()

    if form.validate_on_submit():
        phone_number = form.phone_number.data
        duration = form.duration.data
        event = form.event.data

        # Get registration time
        hour = int(form.hour.data)
        minute = int(form.minute.data)
        am_pm = form.am_pm.data

        # Adjust for DateTime 24 hour time
        if am_pm == 'PM' and hour != 12:
            hour += 12
        elif am_pm == 'AM' and hour == 12:
            hour = 0

        try:
            today = datetime.date.today()
 
            registration_time = datetime.datetime(
                today.year, today.month, today.day,
                hour, minute, 0
            )

            # Local time zone
            local_time_zone = datetime.datetime.now().astimezone().tzinfo

            local_registration_time = registration_time.replace(tzinfo=local_time_zone)

            # Convert to UTC
            registration_time_utc = local_registration_time.astimezone(datetime.timezone.utc)

            add_to_queue(phone_number, event, registration_time_utc, duration)
            services.send_confirmation_message(phone_number, event, registration_time_utc, duration)
            return redirect(url_for('sms.test'))
        except Exception as e:
            render_template("showers/register_event.html", form=form, error=e)
            print(e)

    return render_template("showers/register_event.html", form=form)
