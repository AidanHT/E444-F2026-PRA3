"""ECE444 PRA3: Flask forms, Docker, and a chatbot with session memory."""

import os
import secrets
from datetime import UTC, datetime

from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf.csrf import CSRFError, CSRFProtect

from chatbot import MAX_MESSAGE_LENGTH, get_reply
from forms import NameForm

app = Flask(__name__)
app.config["BOOTSTRAP_SERVE_LOCAL"] = True
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY") or secrets.token_hex(32)
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024
bootstrap = Bootstrap(app)
moment = Moment(app)
csrf = CSRFProtect(app)


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
        return redirect(url_for("chatbot_page"))
    return render_template(
        "index.html", form=form, name=session.get("name"), email=session.get("email")
    )


@app.route("/user/<name>")
def user(name):
    """Render a personalized greeting using Jinja's automatic HTML escaping."""
    return render_template("user.html", name=name, current_time=datetime.now(UTC))


@app.get("/chatbot")
def chatbot_page():
    """Show the chat page only after a valid Home form submission."""
    if not session.get("name") or not session.get("email"):
        return redirect(url_for("index"))
    return render_template(
        "chat.html",
        name=session["name"],
        email=session["email"],
        max_message_length=MAX_MESSAGE_LENGTH,
    )


@app.post("/chat")
def chat():
    """Validate a JSON message and return a reply using this browser's session."""
    if not session.get("name") or not session.get("email"):
        return {"error": "Submit your name and UofT email on Home first."}, 401
    if not request.is_json:
        return {"error": "Send a JSON object with a message."}, 415
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return {"error": "Send a JSON object with a message."}, 400
    message = payload.get("message")
    if not isinstance(message, str) or not message.strip():
        return {"error": "Please enter a message."}, 400
    message = message.strip()
    if len(message) > MAX_MESSAGE_LENGTH:
        return {
            "error": f"Messages must be at most {MAX_MESSAGE_LENGTH} characters."
        }, 400
    return {"reply": get_reply(message)}


@app.post("/logout")
def logout():
    """Clear the identity, chatbot memory, and CSRF state before returning Home."""
    session.clear()
    return redirect(url_for("index"))


@app.errorhandler(CSRFError)
def csrf_error(_error):
    """Return a useful error for expired or invalid form tokens."""
    message = "Your form has expired. Reload the page and try again."
    if request.path == url_for("chat"):
        return {"error": message}, 400
    return render_template("error.html", message=message), 400


@app.errorhandler(413)
def request_too_large(_error):
    """Keep oversized chat errors compatible with the JSON client."""
    message = "The request is too large. Please send less text."
    if request.endpoint == "chat":
        return {"error": message}, 413
    return render_template("error.html", message=message), 413


@app.after_request
def prevent_session_page_caching(response):
    """Keep pages with session data out of the browser's response cache."""
    if request.endpoint in {"index", "chatbot_page", "chat", "logout"}:
        response.headers["Cache-Control"] = "no-store"
    return response


if __name__ == "__main__":
    app.run()
