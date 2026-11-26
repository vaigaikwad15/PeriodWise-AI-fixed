"""
PeriodWise AI - Profile Routes
"""

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session
)

from bson import ObjectId
from pymongo.errors import PyMongoError, DuplicateKeyError
import re

from routes import login_required
from database.mongodb import users_collection


# Blueprint
profile_bp = Blueprint("profile", __name__)


# Profile Route
@profile_bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile_page():

    # Get logged-in user ID
    user_id = session.get("user_id")

    # Validate User ID
    try:
        object_id = ObjectId(user_id)

    except (ValueError, TypeError):
        session.clear()
        flash("Invalid session. Please login again.", "warning")
        return redirect(url_for("auth.login"))

    # Fetch User from MongoDB
    try:
        user = users_collection.find_one({
            "_id": object_id
        })

    except PyMongoError:
        flash("Unable to connect to database.", "danger")
        return redirect(url_for("dashboard.dashboard_page"))

    # Check User Exists
    if not user:

        session.clear()

        flash(
            "User not found. Please login again.",
            "warning"
        )

        return redirect(url_for("auth.login"))

    # POST Request
    if request.method == "POST":

        # Get Form Data
        name = request.form.get(
            "user_name", ""
        ).strip()

        email = request.form.get(
            "user_email", ""
        ).strip().lower()

        # Name Validation
        if not name:

            flash(
                "Please enter your name.",
                "danger"
            )

            return redirect(
                url_for("profile.profile_page")
            )

        if len(name) > 100:

            flash(
                "Name must not exceed 100 characters.",
                "danger"
            )

            return redirect(
                url_for("profile.profile_page")
            )

        # Email Validation
        email_pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

        if not email or not re.match(email_pattern, email):

            flash(
                "Please enter a valid email address.",
                "danger"
            )

            return redirect(
                url_for("profile.profile_page")
            )

        if len(email) > 150:

            flash(
                "Email must not exceed 150 characters.",
                "danger"
            )

            return redirect(
                url_for("profile.profile_page")
            )

        # Update MongoDB
        try:

            result = users_collection.update_one(
                {"_id": object_id},
                {
                    "$set": {
                        "name": name,
                        "email": email
                    }
                }
            )

            if result.matched_count == 0:

                flash(
                    "User profile not found.",
                    "danger"
                )

                return redirect(
                    url_for("profile.profile_page")
                )

            # Update Session
            session["user_name"] = name

            flash(
                "Profile updated successfully!",
                "success"
            )

        except DuplicateKeyError:

            flash(
                "This email address is already registered.",
                "danger"
            )

        except PyMongoError:

            flash(
                "Unable to update profile. Please try again.",
                "danger"
            )

        return redirect(
            url_for("profile.profile_page")
        )

    # Remove Password Hash
    user.pop("password_hash", None)

    # Convert ObjectId to String
    user["_id"] = str(user["_id"])

    # Render Profile Page
    return render_template(
        "profile.html",
        user=user,
        user_name=user.get("name", ""),
        user_email=user.get("email", "")
    )