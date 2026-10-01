"""A small rule-based chatbot that stores a remembered name in Flask's session."""

import re

from flask import session

MAX_MESSAGE_LENGTH = 200
MAX_NAME_LENGTH = 100


def get_reply(message: str) -> str:
    """Remember a declared name and recall it on a later request."""
    declaration = re.fullmatch(r"my name is\s+(.+)", message, flags=re.IGNORECASE)
    if declaration:
        name = declaration.group(1).strip().rstrip(".!?").strip()
        if not name:
            return "Please tell me a name after 'My name is'."
        if len(name) > MAX_NAME_LENGTH:
            return "Please use a name of 100 characters or fewer."
        session["chat_name"] = name
        return f"Nice to meet you, {name}!"

    question = message.casefold().rstrip(".!?").strip()
    if question in {"what is my name", "what's my name"}:
        name = session.get("chat_name")
        if name:
            return f"Your name is {name}."
        return "I don't know your name yet. Tell me 'My name is Alice.'"

    if "hello" in message.casefold():
        return "Hello!"

    return "I don't understand."
