# DocAssist+ AI Assistant

## Features
- RAG-based Q&A
- Intent detection
- Emotion detection
- Multi-turn chat

## Setup

### Backend
cd backend
pip install -r requirements.txt
uvicorn main:app --reload

### Frontend
Open index.html in browser

## APIs
- POST /documents/upload
- POST /chat

## Example
User: What is return policy  
Bot: Returns are accepted within 7 days