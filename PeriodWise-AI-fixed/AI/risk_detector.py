"""
PeriodWise AI - Symptom Alert Detector

This module checks user-reported menstrual symptoms
and provides general safety guidance.

It does not diagnose medical conditions.
"""


def detect_symptom_alerts(symptom_data=None):
    """
    Check symptom severity and return appropriate alerts.

    Parameters:
        symptom_data (dict): User-reported symptom scores from 0 to 10.

    Returns:
        dict: Alert level, messages and safety guidance.
    """

    symptom_data = symptom_data or {}

    supported_symptoms = [
        "cramps",
        "headache",
        "fatigue",
        "bloating",
        "back_pain",
        "nausea"
    ]

    alerts = []
    invalid_entries = []

    # -----------------------------------------
    # 1. CHECK SYMPTOM SCORES
    # -----------------------------------------

    for symptom in supported_symptoms:

        if symptom not in symptom_data:
            continue

        severity = symptom_data[symptom]

        # Validate score between 0 and 10.
        if (
            isinstance(severity, bool)
            or not isinstance(severity, (int, float))
            or not 0 <= severity <= 10
        ):
            invalid_entries.append(symptom)
            continue

        symptom_name = symptom.replace("_", " ").title()

        # -----------------------------------------
        # 2. SEVERE SYMPTOMS
        # -----------------------------------------

        if severity >= 8:
            alerts.append({
                "symptom": symptom_name,
                "severity": severity,
                "level": "High",
                "message": (
                    f"You reported severe {symptom_name.lower()}. "
                    "Consider prompt medical advice, especially "
                    "if the pain is unusual or affects daily life."
                )
            })

        # -----------------------------------------
        # 3. MODERATE SYMPTOMS
        # -----------------------------------------

        elif severity >= 5:
            alerts.append({
                "symptom": symptom_name,
                "severity": severity,
                "level": "Moderate",
                "message": (
                    f"You reported moderate {symptom_name.lower()}. "
                    "Keep tracking the symptom and note any changes."
                )
            })

        # -----------------------------------------
        # 4. MILD SYMPTOMS
        # -----------------------------------------

        else:
            alerts.append({
                "symptom": symptom_name,
                "severity": severity,
                "level": "Mild",
                "message": (
                    f"You reported mild {symptom_name.lower()}."
                )
            })

    # -----------------------------------------
    # 5. GENERAL SAFETY GUIDANCE
    # -----------------------------------------

    if invalid_entries:
        alert_level = "Check Input"

    elif any(alert["level"] == "High" for alert in alerts):
        alert_level = "High"

    elif any(alert["level"] == "Moderate" for alert in alerts):
        alert_level = "Moderate"

    else:
        alert_level = "Low"

    safety_message = (
        "Seek urgent medical care for sudden severe pain, fainting, "
        "or very heavy bleeding accompanied by weakness or dizziness. "
        "If symptoms repeatedly disrupt daily activities, consult "
        "a healthcare professional."
    )

    # -----------------------------------------
    # 6. RETURN RESULTS
    # -----------------------------------------

    return {
        "success": True,
        "alert_level": alert_level,
        "alerts": alerts,
        "invalid_entries": invalid_entries,
        "safety_message": safety_message,
        "disclaimer": (
            "This tool provides general safety guidance only. "
            "It does not diagnose or rule out any medical condition."
        )
    }