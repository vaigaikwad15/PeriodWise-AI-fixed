"""
PeriodWise AI - Prediction Service

Connects cycle records with the AI prediction module.
"""

from models.cycle_model import get_cycles_by_user
from AI.cycle_predictor import predict_next_period


def predict_user_next_period(user_id):
    """
    Predict the next period using a user's recorded cycles.

    Requires at least two different period start dates.
    """

    if not isinstance(user_id, str) or not user_id.strip():
        return {
            "success": False,
            "message": "A valid user ID is required."
        }

    cycles = get_cycles_by_user(user_id)

    if not cycles:
        return {
            "success": False,
            "message": (
                "No cycle records found. "
                "Please record your period dates first."
            )
        }

    period_dates = [
        cycle["period_start_date"]
        for cycle in cycles
        if cycle.get("period_start_date")
    ]

    prediction = predict_next_period(period_dates)

    return prediction