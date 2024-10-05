"""
The function login_required on this file (helpers.py) is cited from CS50 Week9 project "finance"
"""
from flask import redirect, session
from functools import wraps


def login_required(f):
    """
    Decorate routes to require login.
    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function


def get_user_name(db, session):
    if session.get("user_id") is None:
        return ""
    else:
        name = db.execute(
            "SELECT * FROM users WHERE user_id = ?", (session.get("user_id"), )
        ).fetchone()
    return name[1].capitalize()
