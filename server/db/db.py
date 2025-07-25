from sqlmodel import create_engine, SQLModel
from server.models import *
import os

database_url = os.getenv('DB_CONNECTION_STRING')

# # engine is an object that handles communication with the database
# # echo prints out all statements executed in SQL, helps us debug and understand what's happening
engine = create_engine(database_url, echo=True)

def create_db_and_tables():
    # SQLModel class has attribute metadata where it contains
    # all the informations/table registered. For for instance
    # User table inherits from SQLModel and has table
    # set to true. This table is then registered in SQLModel.metadata
    # so using create_all method we can create the database and all tables
    # registered in the metadata object
    SQLModel.metadata.create_all(engine)

create_db_and_tables()