from app import create_app
from app.models import User
from app.extensions import db

app = create_app()

with app.app_context():
    users = User.query.all()
    print("\nAll Users in Database:")
    print("-" * 50)
    for user in users:
        print(f"ID: {user.id}")
        print(f"Username: {user.username}")
        print(f"School: {user.school}")
        print(f"Dorm: {user.dorm}")
        print("-" * 50)