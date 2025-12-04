# src/models/user.py
from dataclasses import dataclass
from typing import Optional


@dataclass
class User:
    id: Optional[int]
    username: str
    password_hash: str
    role: str = "user"

    def to_row(self):
        return (self.username, self.password_hash, self.role)

    @staticmethod
    def from_row(row):
        if row is None:
            return None
        try:
            _id = row["id"]
            return User(
                id=_id,
                username=row["username"],
                password_hash=row["password_hash"],
                role=row["role"],
            )
        except Exception:
            _id, username, password_hash, role = row
            return User(id=_id, username=username, password_hash=password_hash, role=role)
