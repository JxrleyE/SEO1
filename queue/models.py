from app import db


class QueueEntry(db.Model):
    '''
    Information about QueueEntry for Queue db
    '''
    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(20), nullable=False, index=True)
    registration_time = db.Column(db.DateTime, nullable=False)
    position = db.Column(db.Integer, nullable=False)

