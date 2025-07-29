from typing import Optional
from sqlmodel import Field, SQLModel
import uuid

class User(SQLModel, table=True):
    # uses Optional because this way database can generate id for us and 
    # the editor can help us detect the use of an object that is not saved in the database
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key = True)
    email_addr: str = Field(index=True)
    credential : str # credential(similar to a password) to continue accessing the Google's api until it expires
    