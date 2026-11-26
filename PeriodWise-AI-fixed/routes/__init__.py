"""
PeriodWise AI - Routes Package
"""

from functools import wraps

from flask import session, redirect, url_for, flash


def login_required(view_function):
    """Allow access only to authenticated users."""

    @wraps(view_function)
    def wrapper(*args, **kwargs):

        if not session.get("user_id"):
            flash("Please log in to continue.", "warning")
            return redirect(url_for("auth.login"))

        return view_function(*args, **kwargs)

    return wrapper