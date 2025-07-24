from app import db
from app_queue.models import QueueEntry
from sqlalchemy import func, asc


def add_to_queue(phone_number: str, registration_time: str):
    '''
    Adds user to queue db with position and id
    '''
    # Scan for highest position and increment
    max_position = db.session.query(func.max(QueueEntry.position_in_queue)).scalar()
    new_position = (max_position or 0) + 1

    
    new_queue_entry = QueueEntry(
                                id=form.username.data,
                                phone_number=phone_number,
                                registration_time=registration_time,
                                position=new_position
                                )

        # Save to db
        db.session.add(new_queue_entry)
        db.session.commit()