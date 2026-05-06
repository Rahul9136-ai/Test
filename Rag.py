from sentence_transformers import SentenceTransformer
import numpy as np

model = None
documents = []
vectors = []

faq = {
    "return policy": "Returns are accepted within 7 days. Refunds are processed within 5 days.",
    "refund policy": "Returns are accepted within 7 days. Refunds are processed within 5 days."
}

def get_model():
    global model
    if model is None:
        model = SentenceTransformer("all-MiniLM-L6-v2")
    return model

def store_document(text):
    chunks = [text[i:i+200] for i in range(0, len(text), 200)]
    for chunk in chunks:
        documents.append(chunk)
        vectors.append(get_model().encode(chunk))

def retrieve(query):
    if not vectors:
        return []

    q_vec = get_model().encode(query)
    scores = [np.dot(q_vec, v) for v in vectors]
    top_idx = np.argsort(scores)[-3:]
    return [documents[i] for i in reversed(top_idx)]

def process_query(query, intent, emotion, session):
    query_lower = query.lower()
    for key, answer in faq.items():
        if key in query_lower:
            response = answer
            break
    else:
        context = " ".join(retrieve(query))
        response = context if context else "No data found."

    if emotion == "Angry":
        response = "We sincerely apologize. " + response

    return response

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

