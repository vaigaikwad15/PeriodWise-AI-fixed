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
from pymongo.errors import PyMongoError

from routes import login_required
from database.mongodb import users_collection


profile_bp = Blueprint("profile", __name__)


@profile_bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile_page():

    user_id = session["user_id"]

    try:
        user = users_collection.find_one({
            "_id": ObjectId(user_id)
        })

    except (ValueError, TypeError, PyMongoError):
        user = None

    if not user:
        session.clear()
        flash("Please log in again.", "warning")
        return redirect(url_for("auth.login"))

    if request.method == "POST":

        name = request.form.get("name", "").strip()

        if not name or len(name) > 100:
            flash(
                "Please enter a name of up to 100 characters.",
                "danger"
            )
            return redirect(url_for("profile.profile_page"))

        try:
            users_collection.update_one(
                {"_id": ObjectId(user_id)},
                {"$set": {"name": name}}
            )

            session["user_name"] = name

            flash("Profile updated successfully.", "success")

        except PyMongoError:
            flash("Unable to update profile.", "danger")

        return redirect(url_for("profile.profile_page"))

    # Never send the password hash to the template.
    user.pop("password_hash", None)
    user["_id"] = str(user["_id"])

    return render_template(
        "profile.html",
        user=user
    )