from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List
from src.db import *

# Create FastAPI instance
app = FastAPI()


# Welcome Route
@app.get("/")
def welcome():
    return {"message": "Welcome to my note store room."}

# Create a Single Note
@app.post("/notes/{title}/{content}")
def create_note(title: str, content: str, db: Session = Depends(get_db)):
    note = Note(title=title, content=content)
    db.add(note)
    db.commit()
    db.refresh(note)
    return {
        "message": "Note created successfully",
        "note": {
            "id": note.id,
            "title": note.title,
            "content": note.content,
        },
    }

# Bulk Create Notes
@app.post("/notes/", response_model=dict)
def create_notes(notes: List[NoteCreate], db: Session = Depends(get_db)):
    new_notes = [Note(title=n.title, content=n.content) for n in notes]
    db.add_all(new_notes)
    db.commit()
    return {"message": "Notes added successfully!"}

# Get All Notes (Descending Order)
@app.get("/notes/", response_model=List[NoteSchema])
def get_notes(db: Session = Depends(get_db)):
    notes = db.query(Note).order_by(desc(Note.id)).all()
    return notes

# Get Single Note
@app.get("/notes/{note_id}", response_model=NoteSchema)
def get_note(note_id: int, db: Session = Depends(get_db)):
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

# Update Note
@app.put("/notes/{note_id}", response_model=dict)
def update_note(note_id: int, title: str, content: str, db: Session = Depends(get_db)):
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    note.title = title
    note.content = content
    db.commit()
    db.refresh(note)
    return {
        "message": "Note updated successfully",
        "note": {
            "id": note.id,
            "title": note.title,
            "content": note.content
        },
    }

# Delete Note
@app.delete("/notes/{note_id}")
def delete_note(note_id: int, db: Session = Depends(get_db)):
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    db.delete(note)
    db.commit()
    return {"message": "Note deleted successfully"}
