from typing import Annotated
from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.encoders import jsonable_encoder
import jsonpickle

from server.api import auth as authorize
from server.api import mail_api
from server.db.redis import rd

import jwt
import os

app = FastAPI()

JWT_SECRET = os.getenv("JWT_SECRET")


async def verify_user(request: Request):
    access_token = request.cookies.get("access_token")
    if not access_token:
        # 401 means the user is not authenticated
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )
    else:
        access_token = request.cookies["access_token"]

        # decode access_token
        decoded_jwt = jwt.decode(access_token, JWT_SECRET, algorithms=["HS256"])
        credentails = decoded_jwt["credentials"]
        credentails = authorize.to_credentials_object(credentails)

        if not authorize.is_credentials_valid(credentails):
            # if credentials is not valid anymore notify the user
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
            )

        user_email = decoded_jwt["user_email"]

        return {"user_email": user_email, "credentials": credentails}


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

    jwt_token = authorize.store_credentials(email, credential)
    response = RedirectResponse("/home")
    response.set_cookie(key="access_token", value=jwt_token, httponly=True)
    return response


@app.get("/home")
def home(user_info: Annotated[dict, Depends(verify_user)]):
    user_email = user_info["user_email"]
    credentials = user_info["credentials"]
    mails = rd.get(user_email)
    if mails is None:
        mails = mail_api.getMessages(user_email, credentials)
        rd.set(user_email, jsonpickle.dumps(mails))
    else:
        mails = jsonpickle.loads(mails)
    json_compatible_data = jsonable_encoder(mails)
    return JSONResponse(content=json_compatible_data)
