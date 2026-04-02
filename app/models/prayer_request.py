from datetime import datetime, timezone
from app.extensions import db


class PrayerRequest(db.Model):
    __tablename__ = 'prayer_requests'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=True)  # nullable for anonymous
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    request = db.Column(db.Text, nullable=False)
    is_anonymous = db.Column(db.Boolean, default=False)
    is_public = db.Column(db.Boolean, default=False)  # show on public prayer wall
    status = db.Column(db.String(20), default='new', index=True)  # new, praying, answered
    notes = db.Column(db.Text)  # internal pastor/team notes
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    @property
    def display_name(self):
        if self.is_anonymous or not self.name:
            return 'Anonymous'
        return self.name

    def __repr__(self):
        return f'<PrayerRequest {self.id} - {self.status}>'
