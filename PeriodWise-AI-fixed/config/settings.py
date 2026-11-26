"""
PeriodWise AI - Application Settings

This file manages application configuration
and environment variables.
"""

import os
from dotenv import load_dotenv


# Load environment variables from .env
load_dotenv()


# -----------------------------------------
# APPLICATION INFORMATION
# -----------------------------------------

APP_NAME = os.getenv(
    "APP_NAME",
    "PeriodWise AI"
)

APP_VERSION = "1.0.0"


# -----------------------------------------
# FLASK CONFIGURATION
# -----------------------------------------

DEBUG = os.getenv(
    "DEBUG",
    "True"
).lower() == "true"


HOST = os.getenv(
    "HOST",
    "127.0.0.1"
)


PORT = int(
    os.getenv(
        "PORT",
        "5000"
    )
)


# -----------------------------------------
# DATABASE CONFIGURATION
# -----------------------------------------

MONGODB_URI = os.getenv(
    "MONGODB_URI",
    "mongodb://localhost:27017"
)


DATABASE_NAME = os.getenv(
    "DATABASE_NAME",
    "periodwise_ai"
)


# -----------------------------------------
# SECURITY CONFIGURATION
# -----------------------------------------

SECRET_KEY = os.getenv(
    "SECRET_KEY"
)

if not SECRET_KEY:
    if DEBUG:
        SECRET_KEY = "development-only-secret-key"

    else:
        raise RuntimeError(
            "SECRET_KEY must be configured in the .env file."
        )