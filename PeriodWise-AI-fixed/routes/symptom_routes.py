"""
PeriodWise AI - Symptom Routes
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

from routes import login_required

from models.symptom_model import (
    add_symptom_record,
    get_symptoms_by_user
)

from AI.symptom_analyzer import analyze_symptoms
from AI.risk_detector import detect_symptom_alerts


symptom_bp = Blueprint("symptom", __name__)


@symptom_bp.route("/symptoms", methods=["GET", "POST"])
@login_required
def symptoms_page():

    user_id = session["user_id"]

    if request.method == "POST":

        symptom_names = [
            "cramps",
            "headache",
            "fatigue",
            "bloating",
            "back_pain",
            "nausea"
        ]

        symptoms = {}

        try:
            for name in symptom_names:

                value = request.form.get(name, "").strip()

                if value:
                    symptoms[name] = float(value)

        except ValueError:
            flash("Please enter valid symptom scores.", "danger")
            return redirect(url_for("symptom.symptoms_page"))

        record_date = request.form.get(
            "record_date", ""
        ).strip() or None

        result = add_symptom_record(
            user_id=user_id,
            symptoms=symptoms,
            record_date=record_date
        )

        if result.get("success"):
            flash("Symptoms saved successfully.", "success")
        else:
            flash(result.get("message", "Unable to save symptoms."), "danger")

        return redirect(url_for("symptom.symptoms_page"))

    records = get_symptoms_by_user(user_id)

    # The analyzer expects a list of symptom dictionaries.
    symptom_history = [
        record.get("symptoms", {})
        for record in records
    ]

    analysis = analyze_symptoms(symptom_history)

    # Alerts are generated from the latest record only.
    latest_symptoms = (
        records[0].get("symptoms", {})
        if records
        else {}
    )

    alerts = detect_symptom_alerts(latest_symptoms)

    return render_template(
        "symptoms.html",
        records=records,
        analysis=analysis,
        alerts=alerts
    )