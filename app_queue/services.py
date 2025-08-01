from app import db
from app_queue.models import QueueEntry
from sqlalchemy import func, asc
from datetime import datetime
from flask_login import current_user


def add_to_queue(phone_number: str, event: str, shower_id: int, registration_time: str, duration: int, clicked_time):
    '''
    Adds user to queue db with position and id
    '''

    # Convert registratoin time back into a from that the db would accept
    today = datetime.now().strftime('%Y-%m-%d')
    registration_time = datetime.strptime(f'{today} {registration_time}', '%Y-%m-%d %H:%M:%S')

    # Scan for highest position and increment
    max_position = db.session.query(func.max(QueueEntry.position)).filter_by(event_type=event).scalar()
    new_position = (max_position or 0) + 1

    # # Check for existing phone number for certain event
    existing_entry = QueueEntry.query.filter_by(phone_number=phone_number, event_type=event).first()
    if existing_entry:
        raise Exception(f"Phone number {phone_number} is already in the queue for {event} at position {existing_entry.position}.")

    
    new_queue_entry = QueueEntry(
                                phone_number=phone_number,
                                event_type=event,
                                registration_time=registration_time,
                                duration=duration,
                                position=new_position,
                                clicked_time=clicked_time,
                                shower_id=shower_id,
                                user_id = current_user.id
                                )

    # Save to db
    db.session.add(new_queue_entry)
    db.session.commit()
    print(f'{phone_number} has registered to {event} at shower {shower_id} at time {registration_time} with duration {duration}.')
    print(new_queue_entry)


 # Check if shower is available at a certain time
def shower_available(shower_id, time_slot):

   
    booking = QueueEntry.query.filter(
        QueueEntry.shower_id == shower_id,
        QueueEntry.clicked_time == time_slot, 
        QueueEntry.event_type == 'shower'
    ).first()

    if booking:
        return False
    else:
        return True

# Find and cancels a users booking
def cancel_queue(queue_id, user_id):
    booking = QueueEntry.query.filter_by(id=queue_id, user_id=user_id).first()

    if booking:
        db.session.delete(booking)
        db.session.commit()
        return True
    else:
        return False