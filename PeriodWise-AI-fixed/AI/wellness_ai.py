"""
PeriodWise AI - Wellness Recommendation Engine

Provides general food, self-care and traditional
wellness suggestions based on reported symptoms.

This module does not diagnose or treat diseases.
"""


def generate_wellness_recommendations(symptoms=None):
    """
    Generate general wellness suggestions.

    Parameters:
        symptoms (dict): User-reported symptom scores from 0 to 10.

    Example:
        {
            "cramps": 8,
            "fatigue": 6,
            "bloating": 4
        }

    Returns:
        dict: Food suggestions, self-care tips and safety guidance.
    """

    symptoms = symptoms or {}

    supported_symptoms = [
        "cramps",
        "fatigue",
        "bloating",
        "headache",
        "back_pain",
        "nausea"
    ]

    recommendations = []

    # -----------------------------------------
    # 1. VALIDATE USER INPUT
    # -----------------------------------------

    valid_symptoms = {}

    for symptom in supported_symptoms:

        if symptom not in symptoms:
            continue

        score = symptoms[symptom]

        if (
            isinstance(score, bool)
            or not isinstance(score, (int, float))
            or not 0 <= score <= 10
        ):
            continue

        valid_symptoms[symptom] = score

    # -----------------------------------------
    # 2. CRAMP COMFORT SUGGESTIONS
    # -----------------------------------------

    if valid_symptoms.get("cramps", 0) >= 5:

        recommendations.append({
            "category": "Self-care",
            "title": "Warmth for menstrual cramps",
            "suggestion": (
                "Try a warm heating pad or hot-water bottle "
                "wrapped in a towel over your lower abdomen. "
                "Avoid direct contact with very hot surfaces."
            ),
            "evidence": "Commonly recommended self-care"
        })

        recommendations.append({
            "category": "Movement",
            "title": "Gentle movement",
            "suggestion": (
                "If comfortable, try gentle walking, stretching "
                "or yoga. Stop if movement worsens your pain."
            ),
            "evidence": "May help some people"
        })

    # -----------------------------------------
    # 3. FATIGUE SUGGESTIONS
    # -----------------------------------------

    if valid_symptoms.get("fatigue", 0) >= 5:

        recommendations.append({
            "category": "Rest",
            "title": "Rest and sleep",
            "suggestion": (
                "Allow time for rest and aim for regular, "
                "adequate sleep."
            ),
            "evidence": "General wellness guidance"
        })

    # -----------------------------------------
    # 4. BLOATING SUGGESTIONS
    # -----------------------------------------

    if valid_symptoms.get("bloating", 0) >= 5:

        recommendations.append({
            "category": "Hydration",
            "title": "Stay hydrated",
            "suggestion": (
                "Drink water regularly and notice whether "
                "particular foods seem to worsen your bloating."
            ),
            "evidence": "General wellness guidance"
        })

    # -----------------------------------------
    # 5. HEADACHE SUGGESTIONS
    # -----------------------------------------

    if valid_symptoms.get("headache", 0) >= 5:

        recommendations.append({
            "category": "Comfort",
            "title": "Take a break",
            "suggestion": (
                "Rest in a quiet environment, drink water "
                "and monitor your headache."
            ),
            "evidence": "General self-care"
        })

    # -----------------------------------------
    # 6. BACK PAIN SUGGESTIONS
    # -----------------------------------------

    if valid_symptoms.get("back_pain", 0) >= 5:

        recommendations.append({
            "category": "Comfort",
            "title": "Gentle warmth",
            "suggestion": (
                "Try gentle warmth on the affected area "
                "and avoid movements that worsen your pain."
            ),
            "evidence": "General self-care"
        })

    # -----------------------------------------
    # 7. NAUSEA SUGGESTIONS
    # -----------------------------------------

    if valid_symptoms.get("nausea", 0) >= 5:

        recommendations.append({
            "category": "Food",
            "title": "Small, simple meals",
            "suggestion": (
                "If tolerated, try smaller meals and sip fluids "
                "regularly. Seek medical advice if you cannot "
                "keep fluids down."
            ),
            "evidence": "General self-care"
        })

    # -----------------------------------------
    # 8. GENERAL FOOD SUGGESTIONS
    # -----------------------------------------

    food_suggestions = [
        {
            "food": "Leafy green vegetables",
            "reason": (
                "Provide nutrients including folate and iron."
            )
        },
        {
            "food": "Lentils and beans",
            "reason": (
                "Provide plant-based iron, protein and fibre."
            )
        },
        {
            "food": "Fruit and vegetables",
            "reason": (
                "Help provide a variety of vitamins, minerals "
                "and fibre."
            )
        },
        {
            "food": "Nuts and seeds",
            "reason": (
                "Provide healthy fats and other nutrients."
            )
        }
    ]

    # -----------------------------------------
    # 9. TRADITIONAL WELLNESS SUGGESTIONS
    # -----------------------------------------

    traditional_tips = [
        {
            "name": "Ginger",
            "suggestion": (
                "Ginger tea or ginger used in food may be "
                "an option if you normally tolerate it."
            ),
            "evidence": (
                "Some clinical studies suggest possible "
                "pain relief, but evidence has limitations."
            )
        },
        {
            "name": "Gentle breathing",
            "suggestion": (
                "Try slow, comfortable breathing and relaxation."
            ),
            "evidence": "General relaxation practice"
        },
        {
            "name": "Gentle yoga",
            "suggestion": (
                "Try comfortable, gentle poses if they do "
                "not increase your discomfort."
            ),
            "evidence": "May help some people"
        }
    ]

    # -----------------------------------------
    # 10. SEVERE SYMPTOM SAFETY CHECK
    # -----------------------------------------

    severe_symptoms = [
        symptom
        for symptom, score in valid_symptoms.items()
        if score >= 8
    ]

    if severe_symptoms:

        safety_message = (
            "You reported a symptom with a severity score of 8/10 "
            "or higher. Consider prompt medical advice, especially "
            "if the symptom is new, worsening or affects daily life. "
            "Seek urgent care for sudden severe pain, fainting, "
            "or very heavy bleeding with weakness or dizziness."
        )

    else:

        safety_message = (
            "If symptoms repeatedly disrupt daily activities, "
            "worsen or concern you, consult a healthcare professional."
        )

    # -----------------------------------------
    # 11. DEFAULT RECOMMENDATION
    # -----------------------------------------

    if not recommendations:

        recommendations.append({
            "category": "General wellness",
            "title": "Take care of yourself",
            "suggestion": (
                "Stay hydrated, eat balanced meals, get enough "
                "rest and keep tracking your symptoms."
            ),
            "evidence": "General wellness guidance"
        })

    # -----------------------------------------
    # 12. FINAL RESPONSE
    # -----------------------------------------

    return {
        "success": True,
        "recommendations": recommendations,
        "food_suggestions": food_suggestions,
        "traditional_tips": traditional_tips,
        "safety_message": safety_message,
        "disclaimer": (
            "These suggestions provide general wellness information. "
            "They are not a diagnosis or a substitute for medical care. "
            "Herbal products may have side effects or interact with "
            "medicines; consult a qualified professional if unsure."
        )
    }