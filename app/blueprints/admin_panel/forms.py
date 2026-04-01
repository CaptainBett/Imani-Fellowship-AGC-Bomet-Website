from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (
    StringField, TextAreaField, BooleanField, SubmitField,
    SelectField, IntegerField, DateTimeLocalField, HiddenField,
)
from wtforms.validators import DataRequired, Optional, Length, Email


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
