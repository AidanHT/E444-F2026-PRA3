"""Chapter 4: validated forms with redirects and user sessions."""

import os
import secrets
from datetime import UTC, datetime

from flask import Flask, flash, redirect, render_template, session, url_for
from flask_bootstrap import Bootstrap
from flask_moment import Moment

from forms import NameForm

app = Flask(__name__)
app.config["BOOTSTRAP_SERVE_LOCAL"] = True
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY") or secrets.token_hex(32)
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
bootstrap = Bootstrap(app)
moment = Moment(app)


@app.route("/", methods=["GET", "POST"])
def index():
    """Save a valid name and UofT email, then redirect after a POST."""
    form = NameForm()
    if form.validate_on_submit():
        if session.get("name") and session["name"] != form.name.data:
            flash("Looks like you have changed your name!")
        if session.get("email") and session["email"] != form.email.data:
            flash("Looks like you have changed your email!")
        session["name"] = form.name.data
        session["email"] = form.email.data
        return redirect(url_for("index"))
    return render_template(
        "index.html", form=form, name=session.get("name"), email=session.get("email")
    )


@app.route("/user/<name>")
def user(name):
    """Render a personalized greeting using Jinja's automatic HTML escaping."""
    return render_template("user.html", name=name, current_time=datetime.now(UTC))


if __name__ == "__main__":
    app.run()
