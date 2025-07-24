from flask import request, render_template, redirect
from app_queue.services import add_to_queue
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
        # Get registration time
        time = f'{form.hour.data}:{form.minute.data} {form.am_pm.data}'
        try:
            add_to_queue(phone_number, time, duration)
            services.send_confirmation_message(phone_number, time, duration)
        except Exception as e:
            render_template("register_event.html", error=e)
            print(e)

    return render_template("register_event.html", form=form)