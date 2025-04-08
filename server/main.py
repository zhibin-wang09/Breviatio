from fastapi import FastAPI
from api import mail
from fastapi.responses import RedirectResponse
from api.auth import *

app = FastAPI()
SCOPES = [
    'openid',
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile'
]

STATE_STORAGE = {}

@app.get("/")
def read_root():
    return {"hello": "world"}

@app.get("/authorize")
def auth():
    url, state = get_authorization_url()
    return RedirectResponse(url)
    

@app.get('/oauthcallback')
def oauthcallback(state, code):
    exchange_code(state, code)
    # TODO: Store into database
    return RedirectResponse('/home')
    
@app.get('home')
def home():
    pass

@app.get("/messages/{userId}")
def getMessagesFrom(userId: str):
    messages = mail.getMessages(userId)
    return {"messages": messages}
