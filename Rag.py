from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

documents = []
vectors = []

def store_document(text):
    chunks = [text[i:i+200] for i in range(0, len(text), 200)]
    for chunk in chunks:
        documents.append(chunk)
        vectors.append(model.encode(chunk))

def retrieve(query):
    q_vec = model.encode(query)
    scores = [np.dot(q_vec, v) for v in vectors]
    top_idx = np.argsort(scores)[-3:]
    return [documents[i] for i in top_idx]

def process_query(query, intent, emotion, session):
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


sessions = {}
