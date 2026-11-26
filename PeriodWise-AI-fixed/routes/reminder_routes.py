"""
PeriodWise AI - Reminder Routes
"""

from datetime import datetime, timezone
from zoneinfo import ZoneInfo

from bson import ObjectId
from pymongo.errors import PyMongoError

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session
)

from routes import login_required
from database.mongodb import reminders_collection


reminder_bp = Blueprint("reminder", __name__)


@reminder_bp.route("/reminders", methods=["GET", "POST"])
@login_required
def reminders_page():

    user_id = session["user_id"]
    user_object_id = ObjectId(user_id)

    if request.method == "POST":

        title = request.form.get("title", "").strip()
        reminder_type = request.form.get("reminder_type", "").strip()
        reminder_date = request.form.get("reminder_date", "").strip()
        reminder_time = request.form.get("reminder_time", "").strip()
        notes = request.form.get("notes", "").strip()

        if not title or not reminder_type or not reminder_date:
            flash("Please fill all required fields.", "danger")
            return redirect(url_for("reminder.reminders_page"))

        try:
            selected_date = datetime.strptime(
                reminder_date, "%Y-%m-%d"
            ).date()

            selected_time = datetime.strptime(
                reminder_time or "09:00", "%H:%M"
            ).time()

            local_datetime = datetime.combine(
                selected_date,
                selected_time
            ).replace(tzinfo=ZoneInfo("Asia/Kolkata"))

            reminder_datetime = local_datetime.astimezone(
                timezone.utc
            )

            if reminder_datetime <= datetime.now(timezone.utc):
                flash("Please choose a future date and time.", "danger")
                return redirect(url_for("reminder.reminders_page"))

            reminders_collection.insert_one({
                "user_id": user_object_id,
                "title": title[:150],
                "reminder_type": reminder_type,
                "reminder_date": reminder_datetime,
                "reminder_time": reminder_time or "09:00",
                "notes": notes,
                "created_at": datetime.now(timezone.utc)
            })

            flash("Reminder saved successfully.", "success")

        except ValueError:
            flash("Invalid reminder date or time.", "danger")

        except PyMongoError:
            flash("Unable to save reminder.", "danger")

        return redirect(url_for("reminder.reminders_page"))

    try:
        reminders = list(
            reminders_collection.find({
                "user_id": user_object_id
            }).sort("reminder_date", 1)
        )

        for reminder in reminders:
            reminder["_id"] = str(reminder["_id"])
            reminder["user_id"] = str(reminder["user_id"])

    except PyMongoError:
        reminders = []
        flash("Unable to load reminders.", "danger")

    return render_template(
        "reminders.html",
        reminders=reminders
    )


@reminder_bp.route(
    "/reminders/delete/<reminder_id>",
    methods=["POST"]
)
@login_required
def delete_reminder(reminder_id):

    try:
        result = reminders_collection.delete_one({
            "_id": ObjectId(reminder_id),
            "user_id": ObjectId(session["user_id"])
        })

        if result.deleted_count:
            flash("Reminder deleted successfully.", "success")
        else:
            flash("Reminder not found.", "warning")

    except (ValueError, TypeError, PyMongoError):
        flash("Unable to delete reminder.", "danger")

    return redirect(url_for("reminder.reminders_page"))