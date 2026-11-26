"""
PeriodWise AI - MongoDB Database Connection

This module connects the Flask application
to MongoDB and provides database collections.
"""

from pymongo import MongoClient
from pymongo.errors import PyMongoError

from config.settings import MONGODB_URI, DATABASE_NAME


# MongoDB client configuration
client = MongoClient(
    MONGODB_URI,
    serverSelectionTimeoutMS=5000
)

# Select the application database
db = client[DATABASE_NAME]


# Database collections
users_collection = db["users"]
cycles_collection = db["cycles"]
symptoms_collection = db["symptoms"]
reminders_collection = db["reminders"]


def check_database_connection():
    """
    Check whether MongoDB is accessible.

    Returns:
        dict: Database connection status.
    """

    try:
        client.admin.command("ping")

        return {
            "success": True,
            "message": "MongoDB connected successfully."
        }

    except PyMongoError as error:

        return {
            "success": False,
            "message": "Unable to connect to MongoDB.",
            "error": str(error)
        }


def close_database_connection():
    """
    Close the MongoDB client connection.
    """

    client.close()