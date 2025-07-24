from app.extensions import db


class QueueEntry(db.Model):
    '''
    Information about QueueEntry for Queue db
    '''
    phone_number = db.Column(db.String(20), primary_key=True, index=True)
    registration_time = db.Column(db.String(20), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    position = db.Column(db.Integer, nullable=False)

