import json
import os
import uuid
from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

DATA_FILE = Path(os.getenv("DATA_DIR", "/data")) / "notes.json"
app = FastAPI(title="Mini Pastebin")


class NoteIn(BaseModel):
    text: str


def load() -> dict:
    return json.loads(DATA_FILE.read_text()) if DATA_FILE.exists() else {}


def save(data: dict) -> None:
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    DATA_FILE.write_text(json.dumps(data))


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/notes", status_code=201)
def create_note(note: NoteIn):
    data = load()
    note_id = uuid.uuid4().hex[:8]
    data[note_id] = note.text
    save(data)
    return {"id": note_id}


@app.get("/notes/{note_id}")
def get_note(note_id: str):
    data = load()
    if note_id not in data:
        raise HTTPException(status_code=404, detail="Not found")
    return {"id": note_id, "text": data[note_id]}