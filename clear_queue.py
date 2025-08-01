from app import create_app
from app.extensions import db
from app_queue.models import QueueEntry

app = create_app()

with app.app_context():
    # Delete all queue entries
    QueueEntry.query.delete()
    db.session.commit()
    print("All queue entries have been cleared!")