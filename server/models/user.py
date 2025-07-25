from typing import Optional
from sqlmodel import Field, SQLModel

class User(SQLModel, table=True):
    # uses Optional because this way database can generate id for us and 
    # the editor can help us detect the use of an object that is not saved in the database
    id: Optional[int] = Field(default=None, primary_key = True)
    email_addr: str = Field(index=True)
    credential : str # credential(similar to a password) to continue accessing the Google's api until it expires
    