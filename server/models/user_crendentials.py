from typing import Annotated, Optional
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select

class User_Credential(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key = True)
    email: str = Field(index=True)
    jwt_token : str # jwt token to verify user identify
    credentials : str # credential(similar to a password) to continue accessing the Google's api until it expires