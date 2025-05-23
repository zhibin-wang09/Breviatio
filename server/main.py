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
    url, _ = get_authorization_url()
    return RedirectResponse(url)
    

# state and code are given by Google's api attached to 
# the query param of the redirect URL. They are used to
# further access the Google api
@app.get('/oauthcallback')
def oauthcallback(state, code):
    credential = exchange_code(state, code)
    # TODO: Store into database
    user_info = get_user_info(credential)
    email = user_info['email']
    
    return RedirectResponse('/home')
    
@app.get('home')
def home():
    
    return {"home"}

@app.get("/messages/{userId}")
def getMessagesFrom(userId: str):
    messages = mail.getMessages(userId)
    return {"messages": messages}
