"""
PeriodWise AI - Wellness Routes
"""

from flask import (
    Blueprint,
    render_template,
    session
)

from routes import login_required

from models.symptom_model import get_symptoms_by_user

from AI.wellness_ai import generate_wellness_recommendations
from AI.insights import generate_insights


wellness_bp = Blueprint("wellness", __name__)


@wellness_bp.route("/wellness")
@login_required
def wellness_page():

    user_id = session["user_id"]

    records = get_symptoms_by_user(user_id)

    latest_symptoms = (
        records[0].get("symptoms", {})
        if records
        else {}
    )

    wellness = generate_wellness_recommendations(
        latest_symptoms
    )

    insights = generate_insights(
        symptom_data=latest_symptoms
    )

    return render_template(
        "wellness.html",
        wellness=wellness,
        insights=insights
    )