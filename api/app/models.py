from sqlmodel import SQLModel, Field
from typing import Optional

class NoteBase(SQLModel):
    title: str
    content: Optional[str] = None

class Note(NoteBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

class NoteCreate(NoteBase):
    pass

class NoteRead(NoteBase):
    id: int

class NoteUpdate(SQLModel):
    title: Optional[str] = None
    content: Optional[str] = None
