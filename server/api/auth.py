import logging
from google_auth_oauthlib.flow import Flow, InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import os
import jwt
import json
from datetime import datetime, timedelta
import pytz

from sqlmodel import Session, select
from server.models.user import *
from server.db.db import engine

# reference: https://developers.google.com/identity/protocols/oauth2/web-server#python
# reference: https://developers.google.com/identity/protocols/oauth2/web-server#python_2

# Path to client_secrets.json which should contain a JSON document such as:
# {
#   "web": {
#     "client_id": "[[YOUR_CLIENT_ID]]",
#     "client_secret": "[[YOUR_CLIENT_SECRET]]",
#     "redirect_uris": [],
#     "auth_uri": "https://accounts.google.com/o/oauth2/auth",
#     "token_uri": "https://accounts.google.com/o/oauth2/token"
#   }
# }

# Auth logic flow:
# 1. Prompt the authorization url at google's address
# 2. Wait for the user to authorize their permissions for the mail app and give us access to login their account
# 3. Stores user related information in our database for future usage
# 4. Redirect user back to our endpoint and start the application
CLIENTSECRETS_LOCATION = "server/doc/credentials.json"
JWT_SECRET = os.getenv("JWT_SECRET")
REDIRECT_URI = "http://localhost:8000/oauthcallback"
SCOPES = [
    "openid",
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
]


class GetCredentialsException(Exception):
    """Error raised when an error occurred while retrieving credentials."""

    def __init__(self, authorization_url):
        self.authorization_url = authorization_url


class CodeExchangeException(GetCredentialsException):
    """Error raised when a code exchange has failed."""


class NoRefreshTokenException(GetCredentialsException):
    """Error raised when no refresh token has been found."""


class NoUserIdException(Exception):
    """Error raised when no user ID could be retrieved."""


def get_stored_credentials(user_email):
    """Retrieve stored credentials for the provided user ID."""
    # Implement this function to retrieve credentials from your storage (e.g., database).
    # Example: retrieve from a database and use google.auth.credentials.Credentials.from_authorized_user_info(json.loads(stored_json))

    user_credential = None
    with Session(engine) as session:
        # create a sql command to search for a user that matches the user email
        statement = select(User).where(User.email_addr == user_email)

        # the email is restricted to only one but we use one() here
        user = session.exec(statement).one()

        # get the credentials of the user
        user_credential = user.credential

    return Credentials.from_authorized_user_info(user_credential)


def is_credentials_valid(credentials: str | Credentials):
    if isinstance(credentials, Credentials):
        return credentials.valid
    return to_credentials_object(credentials).valid


def to_credentials_object(credentials: str) -> Credentials:
    credentials = json.loads(credentials)
    credentials = Credentials.from_authorized_user_info(credentials)
    return credentials

def store_credentials(user_email, credentials: Credentials):
    """Store OAuth 2.0 credentials in your application's database."""
    # Implement this function to store the credentials, e.g., store in a database.
    # Example: save credentials.to_json() to the database.
    # credentials_json = credentials.to_json()

    # create jwt token
    encoded_jwt = jwt.encode(
        {
            "user_email": user_email,
            "credentials": credentials.token,
            "exp": datetime.now(tz=pytz.utc) + timedelta(days=5),
        },
        JWT_SECRET,
        algorithm="HS256",
    )

    return encoded_jwt


def exchange_code(state, code):
    """Exchange an authorization code for OAuth 2.0 credentials."""
    flow = Flow.from_client_secrets_file(CLIENTSECRETS_LOCATION, SCOPES, state=state)
    flow.redirect_uri = REDIRECT_URI
    try:
        flow.fetch_token(code=code)
        return flow.credentials
    except Exception as error:
        logging.error("An error occurred: %s", error)
        raise CodeExchangeException(None)


def get_user_info(credentials):
    """Send a request to the UserInfo API to retrieve the user's information."""
    try:
        user_info_service = build("oauth2", "v2", credentials=credentials)
        user_info = user_info_service.userinfo().get().execute()
        if user_info and user_info.get("id"):
            return user_info
        else:
            raise NoUserIdException()
    except Exception as error:
        logging.error("An error occurred: %s", error)


def get_authorization_url():
    """Retrieve the authorization URL."""
    flow = Flow.from_client_secrets_file(CLIENTSECRETS_LOCATION, SCOPES)
    flow.redirect_uri = REDIRECT_URI
    authorization_url, state = flow.authorization_url(
        prompt="consent", access__type="offline"
    )
    return authorization_url, state


def get_credentials(authorization_code, state):
    """Retrieve credentials using the provided authorization code."""
    email_address = ""
    try:
        credentials = exchange_code(authorization_code)
        user_info = get_user_info(credentials)
        email_address = user_info.get("email")
        user_id = user_info.get("id")

        if credentials.refresh_token:
            store_credentials(user_id, credentials)
            return credentials
        else:
            credentials = get_stored_credentials(user_id)
            if credentials and credentials.refresh_token:
                return credentials
    except CodeExchangeException as error:
        logging.error("An error occurred during code exchange.")
        error.authorization_url = get_authorization_url(email_address, state)
        raise error
    except NoUserIdException:
        logging.error("No user ID could be retrieved.")

    authorization_url = get_authorization_url(email_address, state)
    raise NoRefreshTokenException(authorization_url)
