import os
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware

# This is the new part: we import the function from the AI Architect's file.
from rag_pipeline import get_jigyasa_response

# --- Initialize the FastAPI App ---
app = FastAPI(title="Jigyasa Backend")

# --- CORS Middleware (Stays the same) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- In-Memory "Notebook" Database ---
# This is our simple, hackathon-friendly database.
notes_db: List[str] = []

# --- API Models (New model for questions) ---
class Note(BaseModel):
    text: str

class Question(BaseModel):
    question: str

# --- API Endpoints ---

@app.post("/add-note")
def add_note(note: Note):
    """Receives text from the bookmarklet and adds it to our notebook."""
    print(f"Received note: {note.text[:50]}...")
    return {"status": "success", "note_count": len(notes_db)}

@app.get("/notes")
def get_notes():
    """A simple endpoint to view all the notes currently in the notebook."""
    return {"notes": notes_db}

# --- THIS IS THE NEW ENDPOINT FOR THE CHAT UI ---
@app.post("/ask")
def ask_question(question: Question):
    """Receives a question, uses the RAG pipeline to get an answer, and returns it."""
    print(f"Received question: {question.question}")

    # --- THIS IS THE NEW CONVERSATIONAL GUARDRAIL ---
    user_input = question.question.lower().strip()
    greetings = ["hello", "hi", "hey", "how are you"]

    if user_input in greetings:
        print("Caught a greeting. Replying directly.")
        return {"answer": "Hello! How can I help you with your research notes today?"}
    # -----------------------------------------------

    if not notes_db:
        return {"answer": "My notebook is empty! Please add some research notes using the bookmarklet first."}
    
    answer = get_jigyasa_response(question=question.question, notes=notes_db)
    print(f"Sending answer: {answer[:50]}...")
    return {"answer": answer}