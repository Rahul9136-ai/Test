from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from rag import process_query, store_document
from intent import detect_intent, detect_emotion
from memory import sessions

app = FastAPI()

# Allow frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/documents/upload")
def upload(data: dict):
    text = data["text"]
    store_document(text)
    return {"status": "Document stored"}

@app.post("/chat")
def chat(data: dict):
    user_id = data["user_id"]
    message = data["message"]

    # Session handling
    if user_id not in sessions:
        sessions[user_id] = {"intent": None, "slots": {}}

    session = sessions[user_id]

    intent = detect_intent(message)
    emotion = detect_emotion(message)

    response = process_query(message, intent, emotion, session)

    return {
        "intent": intent,
        "emotion": emotion,
        "response": response
    }