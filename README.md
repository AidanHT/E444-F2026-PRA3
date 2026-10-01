# ECE444 PRA3: Flask and Docker

Aidan Tran

This repo is a clone of https://github.com/miguelgrinberg/flasky.
The textbook examples use the author's [first-edition code](https://github.com/miguelgrinberg/flasky-first-edition).

This branch contains the Flask activities. Switch to `PRA3_2` for Docker and the chatbot.
Each activity has a separate commit and an `activity-*` tag. The textbook examples
also have `example-2-1`, `example-2-2`, and `example-4-7` tags.

## Run locally

Use Python 3.13. From this folder in Windows Command Prompt:

```bat
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
python -m flask --app hello run
```

Open http://localhost:5000. For PowerShell, activate with
`.\.venv\Scripts\Activate.ps1` instead.

The form accepts a name and a valid email containing `utoronto`. It displays
both after submission and shows an error for other addresses.

## Required screenshots

Activity 1.3: navigation bar, greeting, and local timestamp in `LLLL` format.

![Activity 1.3](docs/screenshots/1.3-greeting.png)

Activity 1.4: first and last name with a non-UofT email.

![Activity 1.4](docs/screenshots/1.4-non-uoft-email.png)
