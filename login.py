from flask import session, redirect
from functools import wraps


def require_login(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if("logged_in" in session):
            return func(*args, **kwargs)
        return redirect('/login')
    return wrapper
