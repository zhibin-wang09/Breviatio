from fastapi import FastAPI
from api import mail
from fastapi.responses import RedirectResponse
from api.auth import *
from starlette.requests import Request

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
    STATE_STORAGE['state'] = state  
    return RedirectResponse(url)
    

@app.get('/oauthcallback')
def oauthcallback(request: Request):
    credentials = exchange_code(STATE_STORAGE['state'], str(request.url))
    # TODO: Store into database
    return {'success'}
    

@app.get("/messages/{userId}")
def getMessagesFrom(userId: str):
    messages = mail.getMessages(userId)
    return {"messages": messages}
