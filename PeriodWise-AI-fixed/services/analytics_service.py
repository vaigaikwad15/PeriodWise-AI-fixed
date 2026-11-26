"""
PeriodWise AI - Analytics Service

Calculates basic cycle statistics and symptom analysis.
"""

from datetime import date

from models.cycle_model import get_cycles_by_user
from models.symptom_model import get_symptoms_by_user

from AI.symptom_analyzer import analyze_symptoms
from AI.insights import generate_insights


def get_user_analytics(user_id):
    """
    Return cycle statistics, symptom analysis and insights.
    """

    if not isinstance(user_id, str) or not user_id.strip():
        return {
            "success": False,
            "message": "A valid user ID is required."
        }

    cycles = get_cycles_by_user(user_id)
    symptom_records = get_symptoms_by_user(user_id)

    # Calculate the number of days between consecutive
    # recorded period start dates.
    period_dates = sorted({
        cycle["period_start_date"]
        for cycle in cycles
        if cycle.get("period_start_date")
    })

    cycle_lengths = []

    for index in range(1, len(period_dates)):

        try:
            current_date = date.fromisoformat(
                period_dates[index]
            )

            previous_date = date.fromisoformat(
                period_dates[index - 1]
            )

        except ValueError:
            continue

        cycle_length = (
            current_date - previous_date
        ).days

        # Use plausible intervals for basic statistics.
        if 15 <= cycle_length <= 60:
            cycle_lengths.append(cycle_length)

    average_cycle_length = None

    if cycle_lengths:
        average_cycle_length = round(
            sum(cycle_lengths) / len(cycle_lengths),
            1
        )

    symptom_history = [
        record.get("symptoms", {})
        for record in symptom_records
    ]

    symptom_analysis = analyze_symptoms(
        symptom_history
    )

    latest_symptoms = (
        symptom_records[0].get("symptoms", {})
        if symptom_records
        else {}
    )

    insights = generate_insights(
        cycle_data={
            "cycle_lengths": cycle_lengths
        },
        symptom_data=latest_symptoms
    )

    return {
        "success": True,
        "total_cycle_records": len(cycles),
        "total_symptom_records": len(symptom_records),
        "cycle_lengths": cycle_lengths,
        "average_cycle_length": average_cycle_length,
        "symptom_analysis": symptom_analysis,
        "insights": insights,
        "message": (
            "Statistics are based on available records. "
            "More records may help reveal personal patterns."
        )
    }