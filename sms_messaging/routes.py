from flask import request, render_template, redirect, url_for
from app_queue.services import add_to_queue
import datetime
from . import sms_bp
from . import forms
from . import services

@sms_bp.route('/test_message', methods=['GET'])
def test_message():
    services.send_confirmation_message()
    return "<h1>Testing sending message!</h1>"


@sms_bp.route('test', methods=['GET', 'POST'])
def test():
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

            add_to_queue(phone_number, event, registration_time, duration)
            services.send_confirmation_message(phone_number, event, registration_time, duration)
            return redirect(url_for('home.dashboard'))
        except Exception as e:
            render_template("register_event.html", form=form, error=e)
            print(e)

    return render_template("register_event.html", form=form)