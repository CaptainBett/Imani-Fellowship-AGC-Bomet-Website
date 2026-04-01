from datetime import datetime, timezone
from app.extensions import db


class TeamMember(db.Model):
    __tablename__ = 'team_members'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(100))
    bio = db.Column(db.Text)
    photo_url = db.Column(db.String(500))
    category = db.Column(db.String(50), nullable=False, index=True)  # pastoral, choir, elder
    ministry_id = db.Column(db.Integer, nullable=True)  # FK to ministries added in Phase 3
    sort_order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    CATEGORIES = [
        ('pastoral', 'Pastoral Team'),
        ('elder', 'Church Elders'),
        ('deacon', 'Deacons'),
        ('choir', 'Choir Members'),
        ('leader', 'Ministry Leaders'),
    ]

    def __repr__(self):
        return f'<TeamMember {self.name}>'
