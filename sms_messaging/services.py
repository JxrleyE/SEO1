import os
from twilio.rest import Client
from dotenv import load_dotenv
from app_queue.models import QueueEntry
from datetime import datetime, timedelta
from flask import current_app
from app.extensions import db

# load environment variables from .env file
load_dotenv()


# .env variables
ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.environ.get("TWILIO_PHONE_NUMBER")
PERSONAL_NUMBER = os.environ.get("PERSONAL_NUMBER")


# create client
client = Client(ACCOUNT_SID, AUTH_TOKEN)


def send_confirmation_message(phone_number, event, registration_time, duration):
    '''
    Notifies user through sms about registration for a queue.

    Args (To be implemented):
        phone_number (str): Number to receive confirmation message.
        registration_time (str): Time of start of event.

    Returns:
        bool: indication of success or failure.
        message = "You have registered for {event (shower, laundry)} at {registration_time}."
    '''
    try:
        message = client.messages.create(
            body=f"You have registered to {event} at {registration_time} with a duration of {duration} minutes!",
            from_=TWILIO_PHONE_NUMBER,
            to=PERSONAL_NUMBER,
        )

        print(f"Successful sending registration message to {phone_number} with {event} at {registration_time}!")
        return True
    except Exception as e:
        print(f'Error occured: {e}')
        return False


def send_reminder_message(app):
    '''
    Reminders user of upcoming appointment (sent in intervals).

    Args (To be implemented):
        phone_number (str): Number to receive reminder message.
        registration_time (str): Time of start of event.

    Returns:
        message = "Reminder: You have registered for {event (shower, laundry)} at {registration_time}, \
                   {time} from now. Current place: {place}."
    '''
    with app.app_context():
        # Query all registration times from database, and compare with current time
        REMINDER_10_MINUTES = 10
        REMINDER_THRESHOLD_MINUTES = 5
        current_utc_time = datetime.utcnow()
        reminder_window_start = current_utc_time
        reminder_window_end = current_utc_time + timedelta(minutes=REMINDER_10_MINUTES)

        # Fetch entries that are approaching within the reminder window,
        # and haven't had a reminder sent within the cooldown period
        # or never had a reminder sent
        entries_for_reminders = QueueEntry.query.filter(
            QueueEntry.registration_time > reminder_window_start,
            QueueEntry.registration_time <= reminder_window_end,
            (QueueEntry.last_reminder_time == None) |
            (QueueEntry.last_reminder_time < current_utc_time - timedelta(minutes=REMINDER_THRESHOLD_MINUTES))
        ).order_by(QueueEntry.event_type, QueueEntry.position).all()

        for entry in entries_for_reminders:
            time_difference = entry.registration_time - current_utc_time
            minutes = time_difference.total_seconds() / 60

            if 0 < minutes <= REMINDER_10_MINUTES:
                try:
                    message = client.messages.create(
                        body=f"Reminder: You have registered to {entry.event_type} at {entry.registration_time.strftime('%I:%M %p')}, {minutes} from now. Current position {entry.position}.",
                        from_=TWILIO_PHONE_NUMBER,
                        to=PERSONAL_NUMBER,
                    )
        
                except Exception as e:
                    print(f'Error occured: {e}')
                    
                print(f'Successfully sent message to {entry.phone_number}')
        
        return True


def send_appointment_message(app):
    '''
    Notifies user about appointment currently happening.

    Args (To be implemented):
        phone_number (str): Number to receive appointment message.
        
    Returns:
        message = "The {event} that you have registered for will be taking place right now! \
                   Have fun!"
    '''
    with app.app_context():
        current_utc_time = datetime.utcnow()
        
        # Define a small window for time around starting time
        time_window_start = current_utc_time - timedelta(seconds=30)
        time_window_end = current_utc_time + timedelta(seconds=30)

        # Query for those with times between the window to send message
        appointments_to_process = QueueEntry.query.filter(
            QueueEntry.registration_time >= time_window_start,
            QueueEntry.registration_time <= time_window_end
        ).all()
        
        for appointment in appointments_to_process:
            try:
                message = client.messages.create(
                    body=f"The {appointment.event_type} you have registered for will be taking place right now! Have Fun!",
                    from_=TWILIO_PHONE_NUMBER,
                    to=PERSONAL_NUMBER,
                )

                event_type_for_update = appointment.event_type
                position_of_removed = appointment.position

                # Remove user from database after message
                db.session.delete(appointment)
                db.session.commit()
                print(f"Entry {appointment.id} ({appointment.phone_number}) removed from queue.")

                # Deincrement all positions by 1
                QueueEntry.query.filter(
                    QueueEntry.event_type == event_type_for_update,
                    QueueEntry.position > position_of_removed
                ).update({QueueEntry.position: QueueEntry.position - 1}, synchronize_session='fetch')
                
                db.session.commit()
                print(f"Positions for {event_type_for_update} after position {position_of_removed} decremented.")
                print("Successful sending appointment message!")

            except Exception as e:
                print(f'Error occured: {e}')
                
    return True
