from app.extensions import db
from sqlalchemy import CheckConstraint, UniqueConstraint, func


class QueueEntry(db.Model):
    '''
    Information about QueueEntry for Queue db
    '''
    __tablename__ = 'sms_queue'
    
    # Auto incrementing id because phone number can be used twice
    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(20), nullable=False, index=True)
    event_type = db.Column(db.String(50), nullable=False)
    registration_time = db.Column(db.DateTime, nullable=False, default=func.now())
    duration = db.Column(db.Integer, nullable=False)
    position = db.Column(db.Integer, nullable=False)
    last_reminder_time = db.Column(db.DateTime, nullable=True)
    shower_id = db.Column(db.Integer, nullable=False)


     # Define constraints
    __table_args__ = (
        # A phone number can only register ONCE for a given event_type at a time
        UniqueConstraint('phone_number', 'event_type', name='uq_phone_number_event_type'),

        # Position is unique
        UniqueConstraint('event_type', 'position', name='uq_event_type_position'),

        # Constraints for duration
        CheckConstraint(duration > 0, name='duration_positive_check'),
        CheckConstraint(duration <= 60, name='duration_max_60_minutes_check'),
    )

    def __repr__(self):
        return f"<QueueEntry Id: {self.id} - PN: {self.phone_number} - Type: {self.event_type} - Time: {self.registration_time} - Pos: {self.position}>"

