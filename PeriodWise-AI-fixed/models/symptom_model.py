"""
PeriodWise AI - Symptom Model

This module stores and retrieves user-reported
menstrual symptoms in MongoDB.
"""

from datetime import datetime, timezone

from bson import ObjectId
from pymongo.errors import PyMongoError

from database.mongodb import symptoms_collection


SUPPORTED_SYMPTOMS = {
    "cramps",
    "headache",
    "fatigue",
    "bloating",
    "back_pain",
    "nausea"
}


def add_symptom_record(user_id, symptoms, record_date=None):
    """
    Save a user's symptom record.

    Symptom severity must be a number from 0 to 10.
    """

    if not isinstance(symptoms, dict) or not symptoms:
        return {
            "success": False,
            "message": "Please provide symptom information."
        }

    if not isinstance(user_id, str):
        return {
            "success": False,
            "message": "Invalid user ID."
        }

    # Validate symptom names and severity scores.
    for symptom, score in symptoms.items():

        if symptom not in SUPPORTED_SYMPTOMS:
            return {
                "success": False,
                "message": f"Unsupported symptom: {symptom}"
            }

        if (
            isinstance(score, bool)
            or not isinstance(score, (int, float))
            or not 0 <= score <= 10
        ):
            return {
                "success": False,
                "message": (
                    f"Invalid score for {symptom}. "
                    "Use a number from 0 to 10."
                )
            }

    try:
        user_object_id = ObjectId(user_id)

        if record_date is None:
            record_date = datetime.now(timezone.utc).date().isoformat()

        elif isinstance(record_date, datetime):
            record_date = record_date.date().isoformat()

        elif hasattr(record_date, "isoformat") and not isinstance(
            record_date, str
        ):
            record_date = record_date.isoformat()

        if not isinstance(record_date, str):
            return {
                "success": False,
                "message": "Date must use YYYY-MM-DD format."
            }

        # Validate the date format.
        from datetime import date

        record_date = date.fromisoformat(record_date).isoformat()

        record = {
            "user_id": user_object_id,
            "record_date": record_date,
            "symptoms": symptoms.copy(),
            "created_at": datetime.now(timezone.utc)
        }

        result = symptoms_collection.insert_one(record)

        return {
            "success": True,
            "record_id": str(result.inserted_id),
            "message": "Symptom record saved successfully."
        }

    except (ValueError, TypeError):
        return {
            "success": False,
            "message": "Invalid user ID or date format."
        }

    except PyMongoError:
        return {
            "success": False,
            "message": "Database error while saving symptoms."
        }


def get_symptoms_by_user(user_id):
    """
    Retrieve all symptom records for a user.
    """

    try:
        user_object_id = ObjectId(user_id)

        records = list(
            symptoms_collection.find(
                {"user_id": user_object_id}
            ).sort("record_date", -1)
        )

        for record in records:
            record["_id"] = str(record["_id"])
            record["user_id"] = str(record["user_id"])

        return records

    except (ValueError, TypeError, PyMongoError):
        return []


def get_symptoms_by_date(user_id, record_date):
    """
    Retrieve a user's symptom records for a specific date.
    """

    try:
        user_object_id = ObjectId(user_id)

        from datetime import date

        if isinstance(record_date, datetime):
            record_date = record_date.date().isoformat()

        elif isinstance(record_date, date):
            record_date = record_date.isoformat()

        if not isinstance(record_date, str):
            return []

        record_date = date.fromisoformat(record_date).isoformat()

        records = list(
            symptoms_collection.find({
                "user_id": user_object_id,
                "record_date": record_date
            })
        )

        for record in records:
            record["_id"] = str(record["_id"])
            record["user_id"] = str(record["user_id"])

        return records

    except (ValueError, TypeError, PyMongoError):
        return []