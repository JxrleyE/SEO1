from app import db
from app_queue.models import QueueEntry
from sqlalchemy import func, asc


def add_to_queue(phone_number: str, event: str, registration_time: str, duration: int):
    '''
    Adds user to queue db with position and id
    '''
    # Scan for highest position and increment
    max_position = db.session.query(func.max(QueueEntry.position)).filter_by(event_type=event).scalar()
    new_position = (max_position or 0) + 1

    # Check for existing phone number for certain event
    existing_entry = QueueEntry.query.filter_by(phone_number=phone_number, event_type=event).first()
    if existing_entry:
        raise Exception(f"Phone number {phone_number} is already in the queue for {event} at position {existing_entry.position}.")

    
    new_queue_entry = QueueEntry(
                                phone_number=phone_number,
                                event_type=event,
                                registration_time=registration_time,
                                duration=duration,
                                position=new_position
                                )

    # Save to db
    db.session.add(new_queue_entry)
    db.session.commit()
    print(new_queue_entry)