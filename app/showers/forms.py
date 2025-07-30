from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, IntegerField
from wtforms.validators import InputRequired, Length, ValidationError, NumberRange


# Form for event registration with validation
class EventRegistrationForm(FlaskForm):
    phone_number = StringField(
        validators=[InputRequired(), Length(min=2, max=20)],
        render_kw={"placeholder": "Phone Number (e.g. +12223334444)"}
    )
    submit = SubmitField('Register')
