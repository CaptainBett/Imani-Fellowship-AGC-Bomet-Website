from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (
    StringField, TextAreaField, BooleanField, SubmitField,
    SelectField, IntegerField, DateTimeLocalField, HiddenField, DateField,
)
from wtforms.validators import DataRequired, Optional, Length, Email, URL


# --- Announcements ---

class AnnouncementForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=200)])
    excerpt = StringField('Excerpt (short summary)', validators=[Optional(), Length(max=500)])
    body = TextAreaField('Content', validators=[DataRequired()])
    image = FileField('Featured Image', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'webp', 'gif'], 'Images only!')
    ])
    is_published = BooleanField('Publish now')
    submit = SubmitField('Save')


# --- Events ---

class EventForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('Description', validators=[Optional()])
    location = StringField('Location', validators=[Optional(), Length(max=200)])
    start_datetime = DateTimeLocalField(
        'Start Date & Time', format='%Y-%m-%dT%H:%M', validators=[DataRequired()]
    )
    end_datetime = DateTimeLocalField(
        'End Date & Time', format='%Y-%m-%dT%H:%M', validators=[Optional()]
    )
    image = FileField('Event Image', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'webp', 'gif'], 'Images only!')
    ])
    is_recurring = BooleanField('Recurring event')
    recurrence_rule = SelectField('Recurrence', choices=[
        ('', 'None'),
        ('WEEKLY', 'Weekly'),
        ('BIWEEKLY', 'Every 2 Weeks'),
        ('MONTHLY', 'Monthly'),
    ], validators=[Optional()])
    is_published = BooleanField('Published', default=True)
    submit = SubmitField('Save')


# --- Team Members ---

class TeamMemberForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(max=100)])
    title = StringField('Title / Role', validators=[Optional(), Length(max=100)])
    bio = TextAreaField('Biography', validators=[Optional()])
    photo = FileField('Photo', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'webp'], 'Images only!')
    ])
    category = SelectField('Category', choices=[
        ('pastoral', 'Pastoral Team'),
        ('elder', 'Church Elders'),
        ('deacon', 'Deacons'),
        ('choir', 'Choir Members'),
        ('leader', 'Ministry Leaders'),
    ], validators=[DataRequired()])
    sort_order = IntegerField('Display Order', default=0, validators=[Optional()])
    is_active = BooleanField('Active', default=True)
    submit = SubmitField('Save')


# --- Pages ---

class PageForm(FlaskForm):
    title = StringField('Page Title', validators=[DataRequired(), Length(max=200)])
    content = TextAreaField('Content', validators=[DataRequired()])
    meta_description = StringField('Meta Description (SEO)', validators=[Optional(), Length(max=300)])
    submit = SubmitField('Save')


# --- Site Settings ---

class SiteSettingsForm(FlaskForm):
    year_theme = StringField('Year Theme', validators=[Optional(), Length(max=200)])
    year_theme_verse = StringField('Year Theme Bible Verse', validators=[Optional(), Length(max=500)])
    whatsapp_number = StringField('WhatsApp Number (e.g. 254712345678)', validators=[Optional(), Length(max=20)])
    church_phone = StringField('Church Phone', validators=[Optional(), Length(max=20)])
    church_email = StringField('Church Email', validators=[Optional(), Email()])
    facebook_url = StringField('Facebook URL', validators=[Optional(), Length(max=500)])
    youtube_url = StringField('YouTube URL', validators=[Optional(), Length(max=500)])
    instagram_url = StringField('Instagram URL', validators=[Optional(), Length(max=500)])
    twitter_url = StringField('Twitter/X URL', validators=[Optional(), Length(max=500)])
    submit = SubmitField('Save Settings')


# --- Ministries ---

class MinistryForm(FlaskForm):
    name = StringField('Ministry Name', validators=[DataRequired(), Length(max=100)])
    slug = StringField('URL Slug', validators=[Optional(), Length(max=100)])
    description = TextAreaField('Description', validators=[Optional()])
    image = FileField('Ministry Image', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'webp', 'gif'], 'Images only!')
    ])
    icon = StringField('Bootstrap Icon Class', validators=[Optional(), Length(max=50)],
                       default='bi-collection')
    sort_order = IntegerField('Display Order', default=0, validators=[Optional()])
    is_active = BooleanField('Active', default=True)
    submit = SubmitField('Save')


class MinistryContentForm(FlaskForm):
    title = StringField('Section Title', validators=[Optional(), Length(max=200)])
    body = TextAreaField('Content', validators=[Optional()])
    image = FileField('Section Image', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'webp', 'gif'], 'Images only!')
    ])
    sort_order = IntegerField('Display Order', default=0, validators=[Optional()])
    submit = SubmitField('Save Section')


# --- Fellowships ---

class FellowshipForm(FlaskForm):
    name = StringField('Fellowship Name', validators=[DataRequired(), Length(max=100)])
    slug = StringField('URL Slug', validators=[Optional(), Length(max=100)])
    description = TextAreaField('Description', validators=[Optional()])
    meeting_day = SelectField('Meeting Day', choices=[
        ('', 'Select day'),
        ('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ], validators=[Optional()])
    meeting_time = StringField('Meeting Time', validators=[Optional(), Length(max=50)])
    location = StringField('Location', validators=[Optional(), Length(max=200)])
    contact_person = StringField('Contact Person', validators=[Optional(), Length(max=100)])
    contact_phone = StringField('Contact Phone', validators=[Optional(), Length(max=20)])
    image = FileField('Fellowship Image', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'webp', 'gif'], 'Images only!')
    ])
    is_active = BooleanField('Active', default=True)
    submit = SubmitField('Save')


# --- Sermons & Devotionals ---

class SermonForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=200)])
    speaker = StringField('Speaker', validators=[Optional(), Length(max=100)])
    series = StringField('Series', validators=[Optional(), Length(max=100)])
    scripture_reference = StringField('Scripture Reference', validators=[Optional(), Length(max=200)])
    excerpt = StringField('Short Summary', validators=[Optional(), Length(max=500)])
    body = TextAreaField('Content / Notes', validators=[Optional()])
    video_url = StringField('Video URL (YouTube/Vimeo)', validators=[Optional(), Length(max=500)])
    audio_url = StringField('Audio URL', validators=[Optional(), Length(max=500)])
    image = FileField('Cover Image', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'webp', 'gif'], 'Images only!')
    ])
    content_type = SelectField('Type', choices=[
        ('sermon', 'Sermon'),
        ('devotional', 'Devotional'),
        ('note', 'Study Note'),
    ], validators=[DataRequired()])
    sermon_date = DateField('Date', validators=[Optional()])
    is_published = BooleanField('Published', default=True)
    is_featured = BooleanField('Featured')
    submit = SubmitField('Save')


# --- Media Gallery ---

class MediaItemForm(FlaskForm):
    title = StringField('Title', validators=[Optional(), Length(max=200)])
    description = TextAreaField('Description', validators=[Optional()])
    media_type = SelectField('Media Type', choices=[
        ('image', 'Image'),
        ('video', 'Video (YouTube/Vimeo URL)'),
    ], validators=[DataRequired()])
    category = SelectField('Category', choices=[
        ('gallery', 'General Gallery'),
        ('choir', 'Choir'),
        ('event', 'Event'),
        ('church', 'Church Life'),
        ('construction', 'Construction'),
    ], validators=[DataRequired()])
    image = FileField('Upload Image', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'webp', 'gif'], 'Images only!')
    ])
    video_url = StringField('Video URL (for video type)', validators=[Optional(), Length(max=500)])
    sort_order = IntegerField('Display Order', default=0, validators=[Optional()])
    is_published = BooleanField('Published', default=True)
    submit = SubmitField('Save')


# --- Giving Categories ---

class GivingCategoryForm(FlaskForm):
    name = StringField('Category Name', validators=[DataRequired(), Length(max=100)])
    slug = StringField('URL Slug', validators=[Optional(), Length(max=100)])
    description = TextAreaField('Description', validators=[Optional()])
    sort_order = IntegerField('Display Order', default=0, validators=[Optional()])
    is_active = BooleanField('Active', default=True)
    submit = SubmitField('Save')
