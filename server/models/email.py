from typing import Optional
from sqlmodel import Field, SQLModel
import json

class Email():
    def __init__(self, date: str, mimeType: str, source: str, to: str, subject: str, snippet: str, body: list[str]):
        self.mimeType = mimeType
        self.source = source
        self.to = to
        self.subject = subject
        self.body = body
        self.snippet = snippet
        self.date = date