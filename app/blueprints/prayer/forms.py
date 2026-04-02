from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Optional, Length, Email


class PrayerRequestForm(FlaskForm):
    name = StringField('Your Name', validators=[Optional(), Length(max=100)])
    email = StringField('Email', validators=[Optional(), Email(), Length(max=120)])
    phone = StringField('Phone', validators=[Optional(), Length(max=20)])
    request = TextAreaField('Prayer Request', validators=[DataRequired(), Length(min=10, max=2000)])
    is_anonymous = BooleanField('Submit anonymously')
    is_public = BooleanField('Allow this request to be shared on the prayer wall')
    submit = SubmitField('Submit Prayer Request')
