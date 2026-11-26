from flask import Blueprint, render_template, session

from routes import login_required

from models.cycle_model import get_cycles_by_user
from models.symptom_model import get_symptoms_by_user

from AI.symptom_analyzer import analyze_symptoms
from AI.insights import generate_insights

from datetime import date


analytics_bp = Blueprint("analytics", __name__)


@analytics_bp.route("/analytics")
@login_required
def analytics_page():

    user_id = session["user_id"]

    cycles = get_cycles_by_user(user_id)
    records = get_symptoms_by_user(user_id)

    # Cycle Length Calculation
    period_dates = [
        cycle["period_start_date"]
        for cycle in cycles
        if cycle.get("period_start_date")
    ]

    cycle_lengths = []

    for index in range(1, len(period_dates)):

        current_date = date.fromisoformat(period_dates[index])
        previous_date = date.fromisoformat(period_dates[index - 1])

        days = (current_date - previous_date).days

        if 15 <= days <= 60:
            cycle_lengths.append(days)

    # Cycle History
    cycle_history = []

    for index, cycle in enumerate(cycles):

        cycle_length = (
            cycle_lengths[index]
            if index < len(cycle_lengths)
            else None
        )

        cycle_history.append({
            "start_date": cycle.get("period_start_date"),
            "end_date": cycle.get("period_end_date"),
            "cycle_length": cycle_length
        })

    # Symptom Data
    symptom_history = [
        record.get("symptoms", {})
        for record in records
    ]

    symptom_analysis = analyze_symptoms(symptom_history)

    latest_symptoms = (
        records[0].get("symptoms", {})
        if records else {}
    )

    symptom_labels = list(latest_symptoms.keys())
    symptom_scores = list(latest_symptoms.values())

    # Average Cycle Length
    average_cycle_length = (
        round(sum(cycle_lengths) / len(cycle_lengths), 1)
        if cycle_lengths else None
    )

    # Average Symptom Severity
    all_scores = [
        score
        for record in records
        for score in record.get("symptoms", {}).values()
        if isinstance(score, (int, float))
        and not isinstance(score, bool)
        and 0 <= score <= 10
    ]

    average_symptom_severity = (
        round(sum(all_scores) / len(all_scores), 1)
        if all_scores else None
    )

    insights = generate_insights(
        cycle_data={"cycle_lengths": cycle_lengths},
        symptom_data=latest_symptoms
    )

    return render_template(
        "analytics.html",
        cycles=cycles,
        records=records,
        cycle_lengths=cycle_lengths,
        cycle_history=cycle_history,
        total_cycles=len(cycles),
        total_symptoms=len(records),
        average_cycle_length=average_cycle_length,
        average_symptom_severity=average_symptom_severity,
        symptom_labels=symptom_labels,
        symptom_scores=symptom_scores,
        symptom_analysis=symptom_analysis,
        insights=insights
    )