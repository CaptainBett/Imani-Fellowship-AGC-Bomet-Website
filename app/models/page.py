from datetime import datetime, timezone
from app.extensions import db


class Page(db.Model):
    __tablename__ = 'pages'

    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(100), unique=True, nullable=False, index=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False, default='')
    meta_description = db.Column(db.String(300))
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
    updated_by = db.Column(db.Integer, db.ForeignKey('users.id'))

    editor = db.relationship('User', backref='edited_pages')

    @staticmethod
    def get_by_slug(slug):
        return Page.query.filter_by(slug=slug).first()

    def __repr__(self):
        return f'<Page {self.slug}>'
