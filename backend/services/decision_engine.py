def classify_ai_score(ai_score):
    if ai_score >= 0.85:
        return "Likely AI-generated"

    if ai_score <= 0.15:
        return "Likely natural"

    return "Uncertain"


def build_analysis_result(ai_score):
    classification = classify_ai_score(ai_score)

    if ai_score >= 0.85 or ai_score <= 0.15:
        confidence = "High"
    else:
        confidence = "Low"

    return {
        "ai_score": ai_score,
        "classification": classification,
        "confidence": confidence,
        "disclaimer": (
            "This result is a model-based assessment and "
            "is not definitive proof of AI generation."
        )
    }