"""
PeriodWise AI - Personalized Insights

This module generates simple personalized insights
from menstrual cycle and symptom information.
"""


def generate_insights(cycle_data=None, symptom_data=None):
    """
    Generate personalized menstrual wellness insights.

    Parameters:
        cycle_data (dict): Information about menstrual cycles.
        symptom_data (dict): User-reported symptom scores.

    Returns:
        dict: Personalized insights and general wellness tips.
    """

    cycle_data = cycle_data or {}
    symptom_data = symptom_data or {}

    insights = []
    wellness_tips = []

    # -----------------------------------------
    # 1. CYCLE LENGTH INSIGHTS
    # -----------------------------------------

    cycle_lengths = cycle_data.get("cycle_lengths", [])

    if cycle_lengths:
        valid_lengths = [
            length
            for length in cycle_lengths
            if isinstance(length, (int, float))
            and not isinstance(length, bool)
            and 1 <= length <= 100
        ]

        if valid_lengths:
            average_length = round(
                sum(valid_lengths) / len(valid_lengths),
                1
            )

            insights.append({
                "category": "Cycle",
                "message": (
                    f"Your recorded average cycle length "
                    f"is {average_length} days."
                )
            })

            if len(valid_lengths) < 3:
                insights.append({
                    "category": "Tracking",
                    "message": (
                        "Record more cycles to understand "
                        "your personal pattern better."
                    )
                })

    # -----------------------------------------
    # 2. SYMPTOM INSIGHTS
    # -----------------------------------------

    supported_symptoms = [
        "cramps",
        "headache",
        "fatigue",
        "bloating",
        "back_pain",
        "nausea"
    ]

    for symptom in supported_symptoms:

        severity = symptom_data.get(symptom)

        if (
            isinstance(severity, bool)
            or not isinstance(severity, (int, float))
            or not 0 <= severity <= 10
        ):
            continue

        symptom_name = symptom.replace("_", " ").title()

        if severity >= 8:
            insights.append({
                "category": "Symptom",
                "message": (
                    f"You reported severe {symptom_name.lower()}. "
                    "Consider seeking medical advice, particularly "
                    "if it is unusual or affects daily activities."
                )
            })

        elif severity >= 5:
            insights.append({
                "category": "Symptom",
                "message": (
                    f"You reported moderate {symptom_name.lower()}. "
                    "Continue tracking this symptom over time."
                )
            })

    # -----------------------------------------
    # 3. GENERAL WELLNESS TIPS
    # -----------------------------------------

    wellness_tips.extend([
        "Stay hydrated throughout the day.",
        "Try a warm heating pad for menstrual cramps.",
        "Get adequate sleep and rest.",
        "Try gentle movement if it feels comfortable.",
        "Eat balanced meals with a variety of nutritious foods."
    ])

    # -----------------------------------------
    # 4. DEFAULT INSIGHT
    # -----------------------------------------

    if not insights:
        insights.append({
            "category": "Getting Started",
            "message": (
                "Start recording your cycle dates and symptoms "
                "to discover personal patterns over time."
            )
        })

    # -----------------------------------------
    # 5. FINAL RESPONSE
    # -----------------------------------------

    return {
        "success": True,
        "insights": insights,
        "wellness_tips": wellness_tips,
        "disclaimer": (
            "These insights are based on the information you record. "
            "They are not a medical diagnosis or a guaranteed prediction."
        )
    }