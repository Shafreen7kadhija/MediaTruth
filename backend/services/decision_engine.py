def classify_ai_score(ai_score):
    if ai_score >= 0.85:
        return "Likely AI-generated"

    if ai_score <= 0.15:
        return "Likely natural"

    return "Uncertain"