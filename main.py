import os
import eel
eel.init('www')
os.system('start chrome -- app='http://localhost:8000')
eel.start('index.html', mode ='chrome', host ='localhost', block='True' size=(800, 600))

from fastapi import FastAPI
from pydantic import BaseModel
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

app = FastAPI()

model = SentenceTransformer("all-MiniLM-L6-v2")

# In-memory storage
vector_store = []
texts = []

class UploadRequest(BaseModel):
    user_id: str
    document_id: str
    text: str

class QueryRequest(BaseModel):
    user_id: str
    query: str

# -------- Chunking --------
def chunk_text(text, chunk_size=100, overlap=20):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunks.append(" ".join(words[i:i+chunk_size]))
    return chunks

# -------- Intent Detection --------
def detect_intent(query):
    if "refund" in query or "not processed" in query:
        return "Complaint"
    return "Question"

# -------- Emotion Detection --------
def detect_emotion(query):
    if "ridiculous" in query or "angry" in query:
        return "Angry"
    return "Neutral"

# -------- Upload API --------
@app.post("/documents/upload")
def upload_doc(req: UploadRequest):
    chunks = chunk_text(req.text)
    embeddings = model.encode(chunks)

    for i, emb in enumerate(embeddings):
        vector_store.append(emb)
        texts.append(chunks[i])

    return {"status": "success", "chunks_stored": len(chunks)}

# -------- Query API --------
@app.post("/query")
def query(req: QueryRequest):
    query_emb = model.encode([req.query])[0]

    scores = []
    for i, vec in enumerate(vector_store):
        score = np.dot(query_emb, vec)
        scores.append((score, texts[i]))

    scores.sort(reverse=True)
    top_chunks = [t[1] for t in scores[:3]]

    intent = detect_intent(req.query)
    emotion = detect_emotion(req.query)

    context = " ".join(top_chunks)

    answer = f"{context}"

    if emotion == "Angry":
        answer = "We apologize for the inconvenience. " + answer

    return {
        "intent": intent,
        "emotion": emotion,
        "answer": answer
    }
    