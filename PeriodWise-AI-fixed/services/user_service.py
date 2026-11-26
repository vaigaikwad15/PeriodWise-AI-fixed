"""
PeriodWise AI - User Service

Handles user registration and authentication.
"""

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from models.user_model import (
    create_user,
    get_user_by_email
)


def register_user(name, email, password):
    """Register a new user securely."""

    if not all(
        isinstance(value, str) and value.strip()
        for value in (name, email, password)
    ):
        return {
            "success": False,
            "message": "All fields are required."
        }

    name = name.strip()
    email = email.strip().lower()

    if len(name) > 100:
        return {
            "success": False,
            "message": "Name must not exceed 100 characters."
        }

    if len(email) > 254 or "@" not in email:
        return {
            "success": False,
            "message": "Please enter a valid email address."
        }

    if len(password) < 8:
        return {
            "success": False,
            "message": "Password must contain at least 8 characters."
        }

    if len(password) > 1024:
        return {
            "success": False,
            "message": "Password is too long."
        }

    existing_user = get_user_by_email(email)

    if existing_user:
        return {
            "success": False,
            "message": "An account with this email already exists."
        }

    password_hash = generate_password_hash(password)

    return create_user(
        name=name,
        email=email,
        password_hash=password_hash
    )


def authenticate_user(email, password):
    """Verify a user's email and password."""

    if not isinstance(email, str) or not isinstance(password, str):
        return {
            "success": False,
            "message": "Invalid email or password."
        }

    user = get_user_by_email(email)

    if not user:
        return {
            "success": False,
            "message": "Invalid email or password."
        }

    password_hash = user.get("password_hash", "")

    if not isinstance(password_hash, str) or not password_hash:
        return {
            "success": False,
            "message": "Invalid email or password."
        }

    if not check_password_hash(password_hash, password):
        return {
            "success": False,
            "message": "Invalid email or password."
        }

    return {
        "success": True,
        "user": user,
        "message": "Login successful."
    }