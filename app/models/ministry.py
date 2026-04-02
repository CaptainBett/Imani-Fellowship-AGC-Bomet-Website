from datetime import datetime, timezone
from app.extensions import db


class Ministry(db.Model):
    __tablename__ = 'ministries'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False, index=True)
    description = db.Column(db.Text)
    image_url = db.Column(db.String(500))
    icon = db.Column(db.String(50), default='bi-collection')  # Bootstrap icon class
    sort_order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    content_sections = db.relationship(
        'MinistryContent', backref='ministry', lazy='dynamic',
        order_by='MinistryContent.sort_order',
        cascade='all, delete-orphan',
    )
    team_members = db.relationship('TeamMember', backref='ministry', lazy='dynamic')

    def __repr__(self):
        return f'<Ministry {self.name}>'


class MinistryContent(db.Model):
    __tablename__ = 'ministry_content'

    id = db.Column(db.Integer, primary_key=True)
    ministry_id = db.Column(db.Integer, db.ForeignKey('ministries.id', ondelete='CASCADE'), nullable=False)
    title = db.Column(db.String(200))
    body = db.Column(db.Text)
    image_url = db.Column(db.String(500))
    sort_order = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'<MinistryContent {self.title}>'
