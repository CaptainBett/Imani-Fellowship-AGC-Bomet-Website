import os
import uuid
from PIL import Image
from flask import current_app
from werkzeug.utils import secure_filename

ALLOWED_IMAGE_EXTENSIONS = {'jpg', 'jpeg', 'png', 'webp', 'gif'}
MAX_IMAGE_WIDTH = 1200
THUMBNAIL_WIDTH = 300


def allowed_image(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS


def save_image(file, subfolder='images'):
    """Save an uploaded image file, resize it, and return the relative URL path."""
    if not file or not file.filename:
        return None

    if not allowed_image(file.filename):
        raise ValueError(f'Invalid image type. Allowed: {", ".join(ALLOWED_IMAGE_EXTENSIONS)}')

    # Generate unique filename
    ext = file.filename.rsplit('.', 1)[1].lower()
    if ext == 'jpeg':
        ext = 'jpg'
    filename = f'{uuid.uuid4().hex}.{ext}'

    # Ensure upload directory exists
    upload_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], subfolder)
    os.makedirs(upload_dir, exist_ok=True)

    filepath = os.path.join(upload_dir, filename)

    # Open with Pillow, resize if needed, save optimized
    img = Image.open(file)

    # Convert RGBA to RGB for JPEG
    if img.mode == 'RGBA' and ext in ('jpg', 'jpeg'):
        img = img.convert('RGB')

    # Resize if wider than max
    if img.width > MAX_IMAGE_WIDTH:
        ratio = MAX_IMAGE_WIDTH / img.width
        new_height = int(img.height * ratio)
        img = img.resize((MAX_IMAGE_WIDTH, new_height), Image.LANCZOS)

    # Save with optimization
    save_kwargs = {'optimize': True}
    if ext in ('jpg', 'jpeg'):
        save_kwargs['quality'] = 80
    img.save(filepath, **save_kwargs)

    # Return URL path relative to static folder
    return f'uploads/{subfolder}/{filename}'


def delete_image(url_path):
    """Delete an image file given its URL path (relative to static/)."""
    if not url_path:
        return

    filepath = os.path.join(
        current_app.root_path, 'static', url_path
    )
    if os.path.exists(filepath):
        os.remove(filepath)
