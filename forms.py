"""Flask-WTF forms for the textbook examples."""

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


def strip_input(value):
    """Remove surrounding whitespace before validating submitted text."""
    return value.strip() if isinstance(value, str) else value


class NameForm(FlaskForm):
    """Validate the name submitted on the Home page."""

    name = StringField(
        "What is your name?",
        filters=[strip_input],
        validators=[DataRequired(), Length(max=100)],
        render_kw={"autocomplete": "name"},
    )
    submit = SubmitField("Submit")
