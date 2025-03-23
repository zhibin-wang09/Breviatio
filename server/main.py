from fastapi import FastAPI
from api import mail

app = FastAPI()

@app.get("/")
def read_root():
    return {"hello": "world"}

@app.get("/auth/google")
def auth():
    pass

@app.get("/messages/{userId}")
def getMessagesFrom(userId: str):
    messages = mail.getMessages(userId)
    return {"messages": messages}
