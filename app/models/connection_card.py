from datetime import datetime, date, timezone
from app.extensions import db


class ConnectionCard(db.Model):
    __tablename__ = 'connection_cards'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    how_heard = db.Column(db.String(100))
    interests = db.Column(db.Text)
    prayer_needs = db.Column(db.Text)
    is_first_visit = db.Column(db.Boolean, default=True)
    visit_date = db.Column(db.Date, default=date.today)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f'<ConnectionCard {self.name}>'
