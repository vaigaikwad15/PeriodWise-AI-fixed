"""
PeriodWise AI - Reminder Service

Creates and retrieves reminder records.
"""

from datetime import datetime, timezone

from bson import ObjectId
from pymongo.errors import PyMongoError

from database.mongodb import reminders_collection


def create_reminder(user_id, title, reminder_date):
    """
    Save a reminder for a user.

    reminder_date must be a datetime object or an ISO datetime string.
    """

    if not isinstance(user_id, str) or not user_id.strip():
        return {
            "success": False,
            "message": "A valid user ID is required."
        }

    if not isinstance(title, str) or not title.strip():
        return {
            "success": False,
            "message": "Reminder title is required."
        }

    title = title.strip()

    if len(title) > 150:
        return {
            "success": False,
            "message": "Reminder title must not exceed 150 characters."
        }

    try:
        user_object_id = ObjectId(user_id)

        if isinstance(reminder_date, str):
            parsed_date = datetime.fromisoformat(
                reminder_date
            )
        elif isinstance(reminder_date, datetime):
            parsed_date = reminder_date
        else:
            return {
                "success": False,
                "message": "Invalid reminder date."
            }

        # Interpret timezone-free datetime values as UTC.
        if parsed_date.tzinfo is None:
            parsed_date = parsed_date.replace(
                tzinfo=timezone.utc
            )

        parsed_date = parsed_date.astimezone(
            timezone.utc
        )

        if parsed_date <= datetime.now(timezone.utc):
            return {
                "success": False,
                "message": "Reminder must be in the future."
            }

        reminder = {
            "user_id": user_object_id,
            "title": title,
            "reminder_date": parsed_date,
            "created_at": datetime.now(timezone.utc),
            "sent": False
        }

        result = reminders_collection.insert_one(
            reminder
        )

        return {
            "success": True,
            "reminder_id": str(result.inserted_id),
            "message": "Reminder created successfully."
        }

    except (ValueError, TypeError):
        return {
            "success": False,
            "message": "Invalid user ID or reminder date."
        }

    except PyMongoError:
        return {
            "success": False,
            "message": "Database error while creating reminder."
        }


def get_user_reminders(user_id):
    """Retrieve all reminders belonging to a user."""

    if not isinstance(user_id, str) or not user_id.strip():
        return []

    try:
        user_object_id = ObjectId(user_id)

        reminders = list(
            reminders_collection.find({
                "user_id": user_object_id
            }).sort("reminder_date", 1)
        )

        for reminder in reminders:
            reminder["_id"] = str(reminder["_id"])
            reminder["user_id"] = str(reminder["user_id"])

        return reminders

    except (ValueError, TypeError, PyMongoError):
        return []


def delete_user_reminder(user_id, reminder_id):
    """
    Delete a reminder only when it belongs to the requesting user.
    """

    try:
        user_object_id = ObjectId(user_id)
        reminder_object_id = ObjectId(reminder_id)

        result = reminders_collection.delete_one({
            "_id": reminder_object_id,
            "user_id": user_object_id
        })

        if result.deleted_count == 1:
            return {
                "success": True,
                "message": "Reminder deleted successfully."
            }

        return {
            "success": False,
            "message": "Reminder not found."
        }

    except (ValueError, TypeError):
        return {
            "success": False,
            "message": "Invalid user or reminder ID."
        }

    except PyMongoError:
        return {
            "success": False,
            "message": "Database error while deleting reminder."
        }