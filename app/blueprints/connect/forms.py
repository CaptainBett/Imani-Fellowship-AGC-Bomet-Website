from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectField, SubmitField
from wtforms.validators import DataRequired, Optional, Length, Email


class ConnectionCardForm(FlaskForm):
    name = StringField('Your Name', validators=[DataRequired(), Length(max=100)])
    email = StringField('Email', validators=[Optional(), Email(), Length(max=120)])
    phone = StringField('Phone Number', validators=[Optional(), Length(max=20)])
    how_heard = SelectField('How did you hear about us?', choices=[
        ('', 'Select one'),
        ('friend', 'Friend or Family'),
        ('social_media', 'Social Media'),
        ('walk_by', 'Walked/Drove By'),
        ('online', 'Online Search'),
        ('event', 'Church Event'),
        ('other', 'Other'),
    ], validators=[Optional()])
    interests = TextAreaField('What are you interested in?', validators=[Optional()],
                              render_kw={'placeholder': 'e.g. Bible study, youth group, choir, volunteering'})
    prayer_needs = TextAreaField('Any prayer requests?', validators=[Optional()],
                                render_kw={'placeholder': 'We would love to pray for you'})
    is_first_visit = BooleanField('This is my first visit', default=True)
    submit = SubmitField('Submit')


class VolunteerForm(FlaskForm):
    name = StringField('Your Name', validators=[DataRequired(), Length(max=100)])
    email = StringField('Email', validators=[Optional(), Email(), Length(max=120)])
    phone = StringField('Phone Number', validators=[DataRequired(), Length(max=20)])
    ministry_id = SelectField('Ministry of Interest', coerce=int, validators=[Optional()])
    message = TextAreaField('Tell us about yourself', validators=[Optional()],
                            render_kw={'placeholder': 'Skills, experience, or anything you\'d like us to know'})
    submit = SubmitField('Sign Up to Volunteer')
