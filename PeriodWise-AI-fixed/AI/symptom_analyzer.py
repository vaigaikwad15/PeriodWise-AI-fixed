"""
PeriodWise AI - Symptom Analyzer

Analyzes historical symptom records and calculates
basic statistics for menstrual wellness tracking.

This module does not diagnose medical conditions.
"""


def analyze_symptoms(symptom_records=None):
    """
    Analyze a list of symptom records.

    Parameters:
        symptom_records (list): List of symptom dictionaries.

    Example:
        [
            {"cramps": 8, "headache": 3},
            {"cramps": 6, "headache": 5}
        ]

    Returns:
        dict: Symptom averages, patterns and summary.
    """

    symptom_records = symptom_records or []

    supported_symptoms = [
        "cramps",
        "headache",
        "fatigue",
        "bloating",
        "back_pain",
        "nausea"
    ]

    symptom_values = {
        symptom: []
        for symptom in supported_symptoms
    }

    invalid_records = 0

    # -----------------------------------------
    # 1. COLLECT VALID SYMPTOM SCORES
    # -----------------------------------------

    for record in symptom_records:

        if not isinstance(record, dict):
            invalid_records += 1
            continue

        for symptom in supported_symptoms:

            if symptom not in record:
                continue

            score = record[symptom]

            if (
                isinstance(score, bool)
                or not isinstance(score, (int, float))
                or not 0 <= score <= 10
            ):
                invalid_records += 1
                continue

            symptom_values[symptom].append(score)

    # -----------------------------------------
    # 2. CALCULATE AVERAGE SCORES
    # -----------------------------------------

    averages = {}

    for symptom, values in symptom_values.items():

        if values:
            averages[symptom] = round(
                sum(values) / len(values),
                2
            )

    # -----------------------------------------
    # 3. IDENTIFY REPEATED OR HIGH SCORES
    # -----------------------------------------

    patterns = []

    for symptom, values in symptom_values.items():

        if not values:
            continue

        high_score_count = sum(
            score >= 7
            for score in values
        )

        if high_score_count >= 2:
            patterns.append({
                "symptom": symptom.replace("_", " ").title(),
                "observation": (
                    f"High scores were recorded on "
                    f"{high_score_count} occasions."
                )
            })

    # -----------------------------------------
    # 4. FIND MOST REPORTED SYMPTOM
    # -----------------------------------------

    most_recorded_symptom = None

    if averages:

        most_recorded_symptom = max(
            averages,
            key=lambda symptom: len(
                symptom_values[symptom]
            )
        )

    # -----------------------------------------
    # 5. CREATE SUMMARY
    # -----------------------------------------

    total_records = len(symptom_records)

    if total_records == 0:
        summary = (
            "No symptom records available. "
            "Start logging your symptoms to view your analysis."
        )

    elif not averages:
        summary = (
            "No valid symptom scores were found. "
            "Check the recorded values."
        )

    else:
        summary = (
            f"Analyzed {total_records} symptom records. "
            "Review the averages and observations "
            "to understand your recorded symptoms."
        )

    # -----------------------------------------
    # 6. RETURN ANALYSIS
    # -----------------------------------------

    return {
        "success": True,
        "total_records": total_records,
        "averages": averages,
        "patterns": patterns,
        "most_recorded_symptom": most_recorded_symptom,
        "invalid_records": invalid_records,
        "summary": summary,
        "disclaimer": (
            "This analysis describes recorded symptoms only. "
            "It does not diagnose a medical condition."
        )
    }