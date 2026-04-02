from datetime import datetime, timezone
from app.extensions import db


class VolunteerSignup(db.Model):
    __tablename__ = 'volunteer_signups'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20), nullable=False)
    ministry_id = db.Column(db.Integer, db.ForeignKey('ministries.id'), nullable=True)
    message = db.Column(db.Text)
    status = db.Column(db.String(20), default='new')  # new, contacted, active
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    ministry = db.relationship('Ministry', backref='volunteer_signups')

    def __repr__(self):
        return f'<VolunteerSignup {self.name}>'
