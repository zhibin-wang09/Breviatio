from typing import List
from training.models.part import Part


class Email:
    def __init__(
        self,
        date: str,
        mimeType: str,
        source: str,
        to: str,
        subject: str,
        body: List[Part],
        snippet="",
    ):
        self.mimeType = mimeType
        self.source = source
        self.to = to
        self.subject = subject
        self.body = body
        self.snippet = snippet
        self.date = date
        self._category = ''

    def __str__(self):
        body_preview = " ".join(self.body[:])
        return (
            f"Email(\n"
            f"  Date: {self.date}\n"
            f"  MIME Type: {self.mimeType}\n"
            f"  Source: {self.source}\n"
            f"  To: {self.to}\n"
            f"  Subject: {self.subject}\n"
            f"  Snippet: {self.snippet}\n"
            f"  Body: {body_preview}\n"
            f")"
    )
        
    @property
    def category(self):
        return self._category
        
    @category.setter
    def category(self, value):
        """The setter for the radius attribute."""
        self._category = value

    def __repr__(self):
        return f"<Email subject='{self.subject}' to='{self.to}' date='{self.date}'>"