from datetime import datetime, timezone
from app.extensions import db


class MediaItem(db.Model):
    __tablename__ = 'media_items'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    description = db.Column(db.Text)
    file_url = db.Column(db.String(500), nullable=False)

    # image, video, audio
    media_type = db.Column(db.String(20), nullable=False, default='image', index=True)

    # Category for grouping: gallery, choir, event, sermon, etc.
    category = db.Column(db.String(50), default='gallery', index=True)

    # Optional link to related entity
    related_type = db.Column(db.String(50))  # e.g. 'event', 'ministry', 'sermon'
    related_id = db.Column(db.Integer)

    sort_order = db.Column(db.Integer, default=0)
    is_published = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    @property
    def is_image(self):
        return self.media_type == 'image'

    @property
    def is_video(self):
        return self.media_type == 'video'

    @property
    def embed_url(self):
        """Convert YouTube/Vimeo URLs to embeddable format."""
        if not self.is_video or not self.file_url:
            return None
        url = self.file_url
        if 'youtube.com/watch' in url:
            video_id = url.split('v=')[1].split('&')[0] if 'v=' in url else None
            return f'https://www.youtube.com/embed/{video_id}' if video_id else url
        if 'youtu.be/' in url:
            video_id = url.split('youtu.be/')[1].split('?')[0]
            return f'https://www.youtube.com/embed/{video_id}'
        if 'vimeo.com/' in url and 'player.vimeo.com' not in url:
            video_id = url.split('vimeo.com/')[1].split('?')[0]
            return f'https://player.vimeo.com/video/{video_id}'
        return url

    def __repr__(self):
        return f'<MediaItem {self.media_type}: {self.title}>'
