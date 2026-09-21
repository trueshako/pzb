from urllib.parse import urlparse

from flask_wtf import FlaskForm
from wtforms import PasswordField, SelectMultipleField, StringField, SubmitField
from wtforms.validators import DataRequired, Length, Optional, ValidationError


INTERESTS = [
    ("acting", "Acting"), ("directing", "Directing"), ("writing", "Screenwriting"),
    ("camera", "Camera"), ("editing", "Editing"), ("film", "African cinema"),
]


class RegistrationForm(FlaskForm):
    display_name = StringField("Display name", validators=[DataRequired(), Length(min=2, max=32)])
    country = StringField("Country or region", validators=[Optional(), Length(max=80)])
    avatar_url = StringField("Avatar image URL (optional)", validators=[Optional(), Length(max=500)])
    interests = SelectMultipleField("Creative interests", choices=INTERESTS, validators=[DataRequired(message="Choose at least one interest.")])
    password = PasswordField("Create a password", validators=[DataRequired(), Length(min=10, max=128)])
    submit = SubmitField("Create my PZB Badge")

    def validate_avatar_url(self, field):
        if not field.data:
            return
        parsed = urlparse(field.data)
        if parsed.scheme != "https" or not parsed.netloc:
            raise ValidationError("Use a full HTTPS image URL, or leave this blank.")


class LoginForm(FlaskForm):
    username = StringField("PZB username", validators=[DataRequired(), Length(max=16)])
    password = PasswordField("Password", validators=[DataRequired(), Length(max=128)])
    submit = SubmitField("Enter PZB")
