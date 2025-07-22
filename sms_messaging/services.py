import os
from twilio.rest import Client
from dotenv import load_dotenv


# load environment variables from .env file
load_dotenv()


# .env variables
ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.environ.get("TWILIO_PHONE_NUMBER")
PERSONAL_NUMBER = os.environ.get("PERSONAL_NUMBER")


# create client
client = Client(ACCOUNT_SID, AUTH_TOKEN)


def send_confirmation_message():
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
            body="This is a test!",
            from_=TWILIO_PHONE_NUMBER,
            to=PERSONAL_NUMBER,
        )

        print("Successful sending registration message!")
        return True
    except Exception as e:
        print(f'Error occured: {e}')
        return False


def send_reminder_message():
    '''
    Reminders user of upcoming appointment (sent in intervals).

    Args (To be implemented):
        phone_number (str): Number to receive reminder message.
        registration_time (str): Time of start of event.

    Returns:
        message = "Reminder: You have registered for {event (shower, laundry)} at {registration_time}, \
                   {time} from now. Current place: {place}."
    '''


def send_appointment_message():
    '''
    Notifies user about appointment currently happening.

    Args (To be implemented):
        phone_number (str): Number to receive appointment message.
        
    Returns:
        message = "The {event} that you have registered for will be taking place right now! \
                   Have fun!"
    '''
