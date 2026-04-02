from datetime import datetime, timezone
from app.extensions import db


class Sermon(db.Model):
    __tablename__ = 'sermons'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), unique=True, nullable=False, index=True)
    speaker = db.Column(db.String(100))
    series = db.Column(db.String(100))
    scripture_reference = db.Column(db.String(200))
    body = db.Column(db.Text)  # Rich text for sermon notes / devotional content
    excerpt = db.Column(db.String(500))

    # Media links (YouTube/Vimeo embeds, external audio URLs)
    video_url = db.Column(db.String(500))
    audio_url = db.Column(db.String(500))
    image_url = db.Column(db.String(500))

    # Type: sermon, devotional, or note
    content_type = db.Column(db.String(20), default='sermon', index=True)

    sermon_date = db.Column(db.Date)
    is_published = db.Column(db.Boolean, default=False)
    is_featured = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def generate_slug(self):
        from re import sub
        base = self.title.lower().strip()
        base = sub(r'[^\w\s-]', '', base)
        base = sub(r'[\s_]+', '-', base)
        base = base.strip('-')
        slug = base
        counter = 1
        while Sermon.query.filter_by(slug=slug).first():
            slug = f'{base}-{counter}'
            counter += 1
        self.slug = slug

    @property
    def embed_url(self):
        """Convert YouTube/Vimeo watch URLs to embeddable URLs."""
        if not self.video_url:
            return None
        url = self.video_url
        # YouTube
        if 'youtube.com/watch' in url:
            video_id = url.split('v=')[1].split('&')[0] if 'v=' in url else None
            return f'https://www.youtube.com/embed/{video_id}' if video_id else url
        if 'youtu.be/' in url:
            video_id = url.split('youtu.be/')[1].split('?')[0]
            return f'https://www.youtube.com/embed/{video_id}'
        # Vimeo
        if 'vimeo.com/' in url and 'player.vimeo.com' not in url:
            video_id = url.split('vimeo.com/')[1].split('?')[0]
            return f'https://player.vimeo.com/video/{video_id}'
        return url

    def __repr__(self):
        return f'<Sermon {self.title}>'
