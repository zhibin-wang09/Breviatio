from typing import Annotated, Optional
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select

class User_Credential(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key = True)
    jwt_token : str
    credentials : str