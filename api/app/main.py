from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import Field, SQLModel, create_engine, Session, select
from typing import Optional, List
from .models import Note, NoteCreate, NoteRead, NoteUpdate
from .db import get_session, init_db

app = FastAPI(title="Notes API")

@app.on_event("startup")
def on_startup():
    init_db()

@app.post("/notes/", response_model=NoteRead)
def create_note(payload: NoteCreate, session: Session = Depends(get_session)):
    note = Note.from_orm(payload)
    session.add(note)
    session.commit()
    session.refresh(note)
    return note

@app.get("/notes/", response_model=List[NoteRead])
def list_notes(limit: int = 50, session: Session = Depends(get_session)):
    stmt = select(Note).limit(limit)
    results = session.exec(stmt).all()
    return results

@app.get("/notes/{note_id}", response_model=NoteRead)
def get_note(note_id: int, session: Session = Depends(get_session)):
    note = session.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

@app.put("/notes/{note_id}", response_model=NoteRead)
def update_note(note_id: int, payload: NoteUpdate, session: Session = Depends(get_session)):
    note = session.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    note_data = payload.dict(exclude_unset=True)
    for key, value in note_data.items():
        setattr(note, key, value)
    session.add(note)
    session.commit()
    session.refresh(note)
    return note

@app.delete("/notes/{note_id}")
def delete_note(note_id: int, session: Session = Depends(get_session)):
    note = session.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    session.delete(note)
    session.commit()
    return {"ok": True}
