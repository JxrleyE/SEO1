from app_queue.models import QueueEntry
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, IntegerField
from wtforms.validators import InputRequired, Length, ValidationError, NumberRange


# Form for event registration with validation
class EventRegistrationForm(FlaskForm):
    phone_number = StringField(
        validators=[InputRequired(), Length(min=2, max=20)],
        render_kw={"placeholder": "Phone Number (e.g. +12223334444)"}
    )
    # Registration time split into 3 parts (hour, minute, AM/PM)
    hour = SelectField(
        'Hour',
        choices=[(str(h), str(h).zfill(2)) for h in range(1, 13)],
        validators=[InputRequired()]
    )
    minute = SelectField(
        'Minute',
        choices=[(str(m), str(m).zfill(2)) for m in range(0, 60)],
        validators=[InputRequired()]
    )
    am_pm = SelectField(
        'AM/PM',
        choices=[('AM', 'AM'), ('PM', 'PM')],
        validators=[InputRequired()]
    )
    duration = IntegerField(
        validators=[InputRequired(),
                    NumberRange(min=10, max=60,
                    message="Duration must be between 10 and 60 minutes.")
        ],
        render_kw={"placeholder": "Duration: (minutes, max 60)"}
    )
    submit = SubmitField('Register')


    # Check if the phone number already exists
    def validate_phone_number(self, phone_number):
        existing_phone_number = QueueEntry.query.filter_by(phone_number=phone_number.data)
        if existing_phone_number:
            raise ValidationError('Phone number already registered!')