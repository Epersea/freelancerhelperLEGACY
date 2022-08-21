import os
from flask import redirect, render_template, request, session
from functools import wraps

# Source: https://cs50.harvard.edu/x/2022/psets/9/finance/
def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def error(message):
    return render_template("error.html", error=message)

# Checks entry exists and is an int
def validate_entry(entry):
    if not entry:
        entry = 0
    else:
        try:
            entry = int(entry)
        except:
            return error("Value should be a number.")
    return entry

