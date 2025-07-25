from typing import Optional
from sqlmodel import Field, SQLModel

class Email(SQLModel, table=True):
    id: Optional[int] = Field(default = None, primary_key = True)
    source: str
    to: str
    subject: str
    body: str
    label: str