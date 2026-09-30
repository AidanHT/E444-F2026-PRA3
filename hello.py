"""Chapter 3: Bootstrap templates and browser-local timestamps."""

from datetime import datetime, timezone

from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_moment import Moment

app = Flask(__name__)
app.config["BOOTSTRAP_SERVE_LOCAL"] = True
bootstrap = Bootstrap(app)
moment = Moment(app)


@app.route("/")
def index():
    """Render the greeting and current UTC time for browser-local formatting."""
    return render_template(
        "index.html", name="Aidan", current_time=datetime.now(timezone.utc)
    )


@app.route("/user/<name>")
def user(name):
    """Render a personalized greeting using Jinja's automatic HTML escaping."""
    return render_template(
        "index.html", name=name, current_time=datetime.now(timezone.utc)
    )


if __name__ == "__main__":
    app.run()
