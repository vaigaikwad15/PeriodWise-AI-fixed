"""
PeriodWise AI - User Model

This module manages user records in MongoDB.
Passwords must be hashed before being stored.
"""

from datetime import datetime, timezone

from bson import ObjectId
from pymongo.errors import PyMongoError

from database.mongodb import users_collection


def create_user(name, email, password_hash):
    """
    Create a new user record.

    password_hash must be a securely generated password hash,
    never a plain-text password.
    """

    if not all(
        isinstance(value, str) and value.strip()
        for value in (name, email, password_hash)
    ):
        return {
            "success": False,
            "message": "Name, email and password hash are required."
        }

    email = email.strip().lower()

    try:
        existing_user = users_collection.find_one(
            {"email": email}
        )

        if existing_user:
            return {
                "success": False,
                "message": "An account with this email already exists."
            }

        user_data = {
            "name": name.strip(),
            "email": email,
            "password_hash": password_hash,
            "created_at": datetime.now(timezone.utc)
        }

        result = users_collection.insert_one(user_data)

        return {
            "success": True,
            "user_id": str(result.inserted_id),
            "message": "User created successfully."
        }

    except PyMongoError:
        return {
            "success": False,
            "message": "Database error while creating user."
        }


def get_user_by_email(email):
    """
    Find a user by email address.
    """

    if not isinstance(email, str) or not email.strip():
        return None

    try:
        user = users_collection.find_one(
            {"email": email.strip().lower()}
        )

        if user:
            user["_id"] = str(user["_id"])

        return user

    except PyMongoError:
        return None


def get_user_by_id(user_id):
    """
    Find a user by MongoDB ObjectId.
    """

    if not isinstance(user_id, str):
        return None

    try:
        object_id = ObjectId(user_id)

        user = users_collection.find_one(
            {"_id": object_id}
        )

        if user:
            user["_id"] = str(user["_id"])

        return user

    except (PyMongoError, ValueError):
        return None