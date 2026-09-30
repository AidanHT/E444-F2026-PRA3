"""Textbook example 2-1: a minimal Flask application."""

from flask import Flask

app = Flask(__name__)


@app.route("/")
def index():
    """Return the Hello World greeting."""
    return "<h1>Hello World!</h1>"


if __name__ == "__main__":
    app.run()
