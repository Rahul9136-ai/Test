def detect_intent(text):
    text = text.lower()
    if "complaint" in text or "not working" in text:
        return "Complaint"
    elif "status" in text:
        return "Check Status"
    return "Query"

def detect_emotion(text):
    text = text.lower()
    if "angry" in text or "ridiculous" in text:
        return "Angry"
    elif "frustrated" in text:
        return "Frustrated"
    return "Neutral"