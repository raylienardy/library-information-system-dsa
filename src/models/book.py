# src/models/book.py
from dataclasses import dataclass, asdict
from typing import List, Optional
import json

@dataclass
class Book:
    id: Optional[int]
    title: str
    author: str
    tags: List[str]
    copies: int = 1

    def to_row(self):
        """Return tuple for DB insertion (title, author, tags_json, copies)."""
        return (self.title, self.author, json.dumps(self.tags), self.copies)

    @staticmethod
    def from_row(row):
        if row is None:
            return None
        # row can be sqlite3.Row or tuple (id, title, author, tags, copies)
        try:
            _id = row["id"]
            title = row["title"]
            author = row["author"]
            tags = json.loads(row["tags"]) if row["tags"] else []
            copies = row["copies"]
        except Exception:
            _id, title, author, tags_text, copies = row
            tags = json.loads(tags_text) if tags_text else []
        return Book(id=_id, title=title, author=author, tags=tags, copies=copies)
