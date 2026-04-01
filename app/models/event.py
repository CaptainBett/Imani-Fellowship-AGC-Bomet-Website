from datetime import datetime, timezone
from app.extensions import db


class Event(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    location = db.Column(db.String(200))
    start_datetime = db.Column(db.DateTime, nullable=False, index=True)
    end_datetime = db.Column(db.DateTime)
    image_url = db.Column(db.String(500))
    is_recurring = db.Column(db.Boolean, default=False)
    recurrence_rule = db.Column(db.String(100))
    is_published = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    @property
    def is_upcoming(self):
        return self.start_datetime > datetime.now(timezone.utc)

    @property
    def formatted_date(self):
        return self.start_datetime.strftime('%B %d, %Y')

    @property
    def formatted_time(self):
        return self.start_datetime.strftime('%I:%M %p')

    def __repr__(self):
        return f'<Event {self.title}>'
