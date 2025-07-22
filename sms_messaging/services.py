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
    Notifies user through sms about registration for a queue
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
