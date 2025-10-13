# core/models.py
from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Dict, Any
from datetime import datetime
import uuid

@dataclass
class Entry:
    id: str
    title: str
    username: str
    password: str
    notes: str = ""
    created_at: str = ""
    updated_at: str = ""

    @staticmethod
    def new(title: str, username: str, password: str, notes: str = "") -> "Entry":
        now = datetime.utcnow().isoformat() + "Z"
        return Entry(
            id=str(uuid.uuid4()),
            title=title,
            username=username,
            password=password,
            notes=notes,
            created_at=now,
            updated_at=now,
        )

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "Entry":
        return Entry(**d)
