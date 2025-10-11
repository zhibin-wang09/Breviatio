class Email:
    def __init__(
        self,
        date: str,
        mimeType: str,
        source: str,
        to: str,
        subject: str,
        body: list,
        snippet="",
    ):
        self.mimeType = mimeType
        self.source = source
        self.to = to
        self.subject = subject
        self.body = body
        self.snippet = snippet
        self.date = date

    def __str__(self):
        body_preview = " ".join(self.body[:2]) + ("..." if len(self.body) > 2 else "")
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

    def __repr__(self):
        return f"<Email subject='{self.subject}' to='{self.to}' date='{self.date}'>"