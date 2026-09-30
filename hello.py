"""Textbook example 2-2: static and dynamic Flask routes."""

from flask import Flask
from markupsafe import escape

app = Flask(__name__)


@app.route("/")
def index():
    """Return the Hello World greeting."""
    return "<h1>Hello World!</h1>"


@app.route("/user/<name>")
def user(name):
    """Greet the name supplied in the URL, escaping it for HTML."""
    return f"<h1>Hello, {escape(name)}!</h1>"


if __name__ == "__main__":
    app.run()
