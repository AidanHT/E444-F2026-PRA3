"""Flask-WTF forms for the textbook examples."""

from flask_wtf import FlaskForm
from wtforms import EmailField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, Length, ValidationError


def strip_input(value):
    """Remove surrounding whitespace before validating submitted text."""
    return value.strip() if isinstance(value, str) else value


class NameForm(FlaskForm):
    """Validate the name and UofT email submitted on the Home page."""

    name = StringField(
        "What is your name?",
        filters=[strip_input],
        validators=[
            DataRequired(),
            Length(max=100, message="Name must be at most 100 characters."),
        ],
        render_kw={"autocomplete": "name"},
    )
    email = EmailField(
        "What is your UofT Email address?",
        filters=[strip_input],
        validators=[
            DataRequired(),
            Email(message="Please enter a valid email address."),
            Length(max=254),
        ],
        render_kw={"autocomplete": "email"},
    )
    submit = SubmitField("Submit")

    def validate_email(self, field):
        """Apply the assignment's case-insensitive 'utoronto' substring rule."""
        if not field.errors and "utoronto" not in field.data.lower():
            raise ValidationError("Please use your UofT email.")
