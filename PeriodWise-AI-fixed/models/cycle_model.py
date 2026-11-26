"""
PeriodWise AI - Cycle Model

This module manages menstrual cycle records in MongoDB.
"""

from datetime import date, datetime, timezone

from bson import ObjectId
from pymongo.errors import PyMongoError

from database.mongodb import cycles_collection


def _parse_date(value):
    """Convert a date or YYYY-MM-DD string into a date object."""

    if isinstance(value, datetime):
        return value.date()

    if isinstance(value, date):
        return value

    if isinstance(value, str):
        return date.fromisoformat(value)

    raise ValueError("Date must use YYYY-MM-DD format.")


def add_cycle(user_id, period_start_date, period_end_date=None):
    """
    Save a menstrual cycle record for a user.

    Dates must be date objects or YYYY-MM-DD strings.
    """

    try:
        user_object_id = ObjectId(user_id)

        start_date = _parse_date(period_start_date)

        end_date = None

        if period_end_date is not None:
            end_date = _parse_date(period_end_date)

        if end_date and end_date < start_date:
            return {
                "success": False,
                "message": "Period end date cannot be before start date."
            }

        cycle_data = {
            "user_id": user_object_id,
            "period_start_date": start_date.isoformat(),
            "period_end_date": (
                end_date.isoformat() if end_date else None
            ),
            "created_at": datetime.now(timezone.utc)
        }

        result = cycles_collection.insert_one(cycle_data)

        return {
            "success": True,
            "cycle_id": str(result.inserted_id),
            "message": "Cycle record saved successfully."
        }

    except (ValueError, TypeError):
        return {
            "success": False,
            "message": "Invalid user ID or date format."
        }

    except PyMongoError:
        return {
            "success": False,
            "message": "Database error while saving cycle."
        }


def get_cycles_by_user(user_id):
    """
    Retrieve all cycle records belonging to a user.
    """

    try:
        user_object_id = ObjectId(user_id)

        cycles = list(
            cycles_collection.find(
                {"user_id": user_object_id}
            ).sort("period_start_date", 1)
        )

        for cycle in cycles:
            cycle["_id"] = str(cycle["_id"])
            cycle["user_id"] = str(cycle["user_id"])

        return cycles

    except (ValueError, TypeError, PyMongoError):
        return []


def get_latest_cycle(user_id):
    """
    Retrieve the most recently started menstrual cycle.
    """

    try:
        user_object_id = ObjectId(user_id)

        cycle = cycles_collection.find_one(
            {"user_id": user_object_id},
            sort=[("period_start_date", -1)]
        )

        if cycle:
            cycle["_id"] = str(cycle["_id"])
            cycle["user_id"] = str(cycle["user_id"])

        return cycle

    except (ValueError, TypeError, PyMongoError):
        return None