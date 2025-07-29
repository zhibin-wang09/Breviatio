from typing import Annotated
from google.oauth2.credentials import Credentials
from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.encoders import jsonable_encoder
import jsonpickle
from datetime import datetime, timezone, timedelta

from server.api import auth as authorize
from server.api import mail_api
from server.db.redis import rd

import os

from server.models.user import User

app = FastAPI()

JWT_SECRET = os.getenv("JWT_SECRET")


async def verify_user(request: Request):
    session_id = request.cookies.get("session_id")
    if not session_id:
        # 401 means the user is not authenticated
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Authentication Credentials",
        )
    else:
        # decode access_token

        user = authorize.get_stored_credentials(session_id)
        credentials = authorize.to_credentials_object(user.credential)

        if not credentials.valid:
            # if credentials is not valid anymore notify the user
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
            )

        return user


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
@app.get("/oauthcallback")
def oauthcallback(state, code):
    credential = authorize.exchange_code(state, code)
    user_info = authorize.get_user_info(credential)
    email = user_info["email"]

    session_id = authorize.store_credentials(email, credential)
    expiry_date = datetime.now(timezone.utc) + timedelta(days=3)
    response = RedirectResponse("/home")
    response.set_cookie(
        key="session_id", value=session_id, httponly=True, expires=expiry_date
    )
    return response


@app.get("/home")
def home(user: Annotated[User, Depends(verify_user)]):
    # mails = rd.get(user_email)
    mails = None
    credentials = authorize.to_credentials_object(user.credential)
    
    if mails is None:
        mails = mail_api.getMessages(user.email_addr, credentials)
        # rd.set(user_email, jsonpickle.dumps(mails))
    else:
        mails = jsonpickle.loads(mails)
    json_compatible_data = jsonable_encoder(mails)
    return JSONResponse(content=json_compatible_data)
