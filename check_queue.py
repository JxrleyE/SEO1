from app import create_app
from app_queue.models import QueueEntry
from app.models import User
from app.extensions import db
from datetime import datetime

app = create_app()

with app.app_context():
    print("\nAll Queue Entries:")
    print("-" * 70)
    entries = QueueEntry.query.all()
    for entry in entries:
        user = User.query.get(entry.user_id)
        username = user.username if user else "No user found"
        print(f"Queue ID: {entry.id}")
        print(f"User ID: {entry.user_id}")
        print(f"Username: {username}")
        print(f"Registration Time: {entry.registration_time}")
        print(f"Shower ID: {entry.shower_id}")
        print("-" * 70)