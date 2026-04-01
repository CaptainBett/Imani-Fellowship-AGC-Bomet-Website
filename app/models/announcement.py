import re
from datetime import datetime, timezone
from app.extensions import db


class Announcement(db.Model):
    __tablename__ = 'announcements'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), unique=True, nullable=False, index=True)
    body = db.Column(db.Text, nullable=False)
    excerpt = db.Column(db.String(500))
    image_url = db.Column(db.String(500))
    is_published = db.Column(db.Boolean, default=False)
    published_at = db.Column(db.DateTime, index=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    author = db.relationship('User', backref='announcements')

    def generate_slug(self):
        slug = re.sub(r'[^\w\s-]', '', self.title.lower())
        slug = re.sub(r'[\s_]+', '-', slug).strip('-')
        # Ensure uniqueness
        base_slug = slug
        counter = 1
        while Announcement.query.filter_by(slug=slug).first():
            slug = f'{base_slug}-{counter}'
            counter += 1
        self.slug = slug

    def publish(self):
        self.is_published = True
        self.published_at = datetime.now(timezone.utc)

    def unpublish(self):
        self.is_published = False
        self.published_at = None

    def __repr__(self):
        return f'<Announcement {self.title}>'
