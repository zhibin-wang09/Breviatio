from fastapi import FastAPI, Request, Cookie, Response
from api import mail
from fastapi.responses import RedirectResponse, JSONResponse
from api import auth as authorize

import jwt
import os
import json

app = FastAPI()
SCOPES = [
    'openid',
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile'
]

JWT_SECRET = os.getenv('JWT_SECRET')

@app.get("/")
def read_root():
    return {"hello": "world"}

@app.get("/authorize")
def auth():
    url, _ = authorize.get_authorization_url()
    return RedirectResponse(url)
    

# state and code are given by Google's api attached to 
# the query param of the redirect URL. They are used to
# further access the Google api
@app.get('/oauthcallback')
def oauthcallback(state, code):
    credential = authorize.exchange_code(state, code)
    # TODO: Store into database
    user_info = authorize.get_user_info(credential)
    email = user_info['email']
    
    jwt_token = authorize.store_credentials(email, credential)
    response = RedirectResponse('/home')
    response.set_cookie(key="access_token", value=jwt_token, httponly=True)
    return response
    
@app.get('/home')
def home(access_token: str = Cookie(None)):
    if access_token:
        # decode access token
        decoded_jwt = jwt.decode(access_token, JWT_SECRET, algorithms=['HS256'])
        credentails = decoded_jwt['credentials']

        if not authorize.is_credentials_valid(credentails):
            # if credentials is not valid anymore notify the user
            return JSONResponse(content={"message": "You need to log in again"}, status_code=401)
        
        user_email = decoded_jwt['user_email']
        return JSONResponse(content={"user": user_email}, status_code=200)
    # 401 means the user is not authenticated 
    return JSONResponse(content={"message": "You are not authenicated"}, status_code=401)

@app.get("/messages/{userId}")
def getMessagesFrom(userId: str):
    messages = mail.getMessages(userId)
    return {"messages": messages}

