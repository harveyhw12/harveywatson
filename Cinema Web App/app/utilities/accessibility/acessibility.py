from flask import session
from app import models

THEME_SESSION_KEY = "theme"


def set_theme(type):
    if type in ["dark", "light", "high-contrast"]:
        session[THEME_SESSION_KEY] = type
        return True
    else:
        return False


def get_theme():
    if THEME_SESSION_KEY not in session:
        session[THEME_SESSION_KEY] = "dark"
    return session[THEME_SESSION_KEY]
