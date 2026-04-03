from datetime import datetime, timezone
from app.extensions import db


class ConstructionUpdate(db.Model):
    __tablename__ = 'construction_updates'

    id = db.Column(db.Integer, primary_key=True)
    phase_name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    percentage = db.Column(db.Integer, default=0)  # 0-100
    image_url = db.Column(db.String(500))
    sort_order = db.Column(db.Integer, default=0)
    is_current = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc),
                           onupdate=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f'<ConstructionUpdate {self.phase_name}>'


class FundraisingGroup(db.Model):
    __tablename__ = 'fundraising_groups'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    target_amount = db.Column(db.Float, default=0)
    raised_amount = db.Column(db.Float, default=0)
    contact_person = db.Column(db.String(100))
    contact_phone = db.Column(db.String(20))
    image_url = db.Column(db.String(500))
    sort_order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    @property
    def progress_percent(self):
        if self.target_amount and self.target_amount > 0:
            return min(round((self.raised_amount / self.target_amount) * 100), 100)
        return 0

    def __repr__(self):
        return f'<FundraisingGroup {self.name}>'
