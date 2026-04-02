from datetime import datetime, timezone
from app.extensions import db


class Fellowship(db.Model):
    __tablename__ = 'fellowships'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False, index=True)
    description = db.Column(db.Text)
    meeting_day = db.Column(db.String(20))
    meeting_time = db.Column(db.String(50))
    location = db.Column(db.String(200))
    contact_person = db.Column(db.String(100))
    contact_phone = db.Column(db.String(20))
    image_url = db.Column(db.String(500))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f'<Fellowship {self.name}>'
