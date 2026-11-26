"""
PeriodWise AI - Wellness Service

Combines symptom history, insights and wellness suggestions.
"""

from models.symptom_model import get_symptoms_by_user

from AI.wellness_ai import generate_wellness_recommendations
from AI.insights import generate_insights
from AI.risk_detector import detect_symptom_alerts


def get_user_wellness(user_id):
    """
    Generate wellness information using the latest symptom record.
    """

    if not isinstance(user_id, str) or not user_id.strip():
        return {
            "success": False,
            "message": "A valid user ID is required."
        }

    records = get_symptoms_by_user(user_id)

    latest_symptoms = {}

    if records:
        latest_symptoms = records[0].get("symptoms", {})

    recommendations = generate_wellness_recommendations(
        latest_symptoms
    )

    insights = generate_insights(
        symptom_data=latest_symptoms
    )

    alerts = detect_symptom_alerts(
        latest_symptoms
    )

    return {
        "success": True,
        "recommendations": recommendations,
        "insights": insights,
        "alerts": alerts,
        "latest_symptoms": latest_symptoms
    }