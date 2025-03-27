from fastapi import FastAPI
from api import mail
from google_auth_oauthlib.flow import InstalledAppFlow

app = FastAPI()
SCOPES = [
    'openid',
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile'
]

@app.get("/")
def read_root():
    return {"hello": "world"}

@app.get("/authorize")
def auth():
    flow = InstalledAppFlow.from_client_secrets_file('./doc/credentials.json',
                                                     scopes=SCOPES)
    flow.redirect_uri = "http://localhost"
    credentials = flow.run_local_server(open_browser=True)
    print(f"CREDENTIALS: {credentials}")
    return {"success"}
    

@app.get("/messages/{userId}")
def getMessagesFrom(userId: str):
    messages = mail.getMessages(userId)
    return {"messages": messages}
