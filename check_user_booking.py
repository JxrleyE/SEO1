from app import create_app
from app.models import User
from app_queue.models import QueueEntry
from app.extensions import db
from datetime import datetime

app = create_app()

def check_user_bookings(username):
    with app.app_context():
        # Find the user
        user = User.query.filter_by(username=username).first()
        if not user:
            print(f"No user found with username: {username}")
            return

        print(f"\nUser Details:")
        print("-" * 50)
        print(f"Username: {user.username}")
        print(f"User ID: {user.id}")
        print(f"School: {user.school}")
        print(f"Dorm: {user.dorm}")
        
        # Get their bookings
        bookings = QueueEntry.query.filter_by(user_id=user.id).all()
        
        print(f"\nBookings for {user.username}:")
        print("-" * 50)
        if not bookings:
            print("No bookings found")
        for booking in bookings:
            print(f"Booking ID: {booking.id}")
            print(f"Shower ID: {booking.shower_id}")
            print(f"Registration Time: {booking.registration_time}")
            print(f"Clicked Time: {booking.clicked_time}")
            print(f"Phone: {booking.phone_number}")
            print("-" * 50)

if __name__ == "__main__":
    username = input("Enter username to check: ")
    check_user_bookings(username)