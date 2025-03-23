import logging
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import os
import json

# reference: https://developers.google.com/identity/protocols/oauth2/web-server#python

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
CLIENTSECRETS_LOCATION = './doc/credentials.json'
REDIRECT_URI = '<YOUR_REGISTERED_REDIRECT_URI>'
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile',
    # 'https://www.googleapis.com/auth/gmail.addons.current.action.compose',
    # 'https://www.googleapis.com/auth/gmail.addons.current.message.action',
    # 'https://www.googleapis.com/auth/gmail.addons.current.message.metadata',
    # 'https://www.googleapis.com/auth/gmail.addons.current.message.readonly',
    # 'https://www.googleapis.com/auth/gmail.labels',
    # 'https://www.googleapis.com/auth/gmail.send',
    # 'https://www.googleapis.com/auth/gmail.compose',
    # 'https://www.googleapis.com/auth/gmail.insert',
    # 'https://www.googleapis.com/auth/gmail.modify',
    # 'https://www.googleapis.com/auth/gmail.metadata',
    # 'https://www.googleapis.com/auth/gmail.settings.basic',
    # 'https://www.googleapis.com/auth/gmail.settings.sharing',
    # 'https://mail.google.com/'
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

def get_stored_credentials(user_id):
    """Retrieve stored credentials for the provided user ID."""
    # Implement this function to retrieve credentials from your storage (e.g., database).
    # Example: retrieve from a database and use google.auth.credentials.Credentials.from_authorized_user_info(json.loads(stored_json))
    raise NotImplementedError()

def store_credentials(user_id, credentials):
    """Store OAuth 2.0 credentials in your application's database."""
    # Implement this function to store the credentials, e.g., store in a database.
    # Example: save credentials.to_json() to the database.
    raise NotImplementedError()

def exchange_code(authorization_code):
    """Exchange an authorization code for OAuth 2.0 credentials."""
    flow = InstalledAppFlow.from_client_secrets_file(CLIENTSECRETS_LOCATION, SCOPES)
    flow.redirect_uri = REDIRECT_URI
    try:
        credentials = flow.fetch_token(authorization_response=authorization_code)
        return credentials
    except Exception as error:
        logging.error('An error occurred: %s', error)
        raise CodeExchangeException(None)

def get_user_info(credentials):
    """Send a request to the UserInfo API to retrieve the user's information."""
    try:
        user_info_service = build('oauth2', 'v2', credentials=credentials)
        user_info = user_info_service.userinfo().get().execute()
        if user_info and user_info.get('id'):
            return user_info
        else:
            raise NoUserIdException()
    except Exception as error:
        logging.error('An error occurred: %s', error)

def get_authorization_url(email_address, state):
    """Retrieve the authorization URL."""
    flow = InstalledAppFlow.from_client_secrets_file(CLIENTSECRETS_LOCATION, SCOPES)
    flow.redirect_uri = "http://localhost"
    authorization_url, _ = flow.authorization_url(prompt='consent', 
                                                  access__type = 'offline', 
                                                  user_id = email_address,
                                                  state=state,)
    return authorization_url

def get_credentials(authorization_code, state):
    """Retrieve credentials using the provided authorization code."""
    email_address = ''
    try:
        credentials = exchange_code(authorization_code)
        user_info = get_user_info(credentials)
        email_address = user_info.get('email')
        user_id = user_info.get('id')

        if credentials.refresh_token:
            store_credentials(user_id, credentials)
            return credentials
        else:
            credentials = get_stored_credentials(user_id)
            if credentials and credentials.refresh_token:
                return credentials
    except CodeExchangeException as error:
        logging.error('An error occurred during code exchange.')
        error.authorization_url = get_authorization_url(email_address, state)
        raise error
    except NoUserIdException:
        logging.error('No user ID could be retrieved.')

    authorization_url = get_authorization_url(email_address, state)
    raise NoRefreshTokenException(authorization_url)

def get_authorization_code(url):
    """Use the authorization url to get the authorization code"""
    pass

def main():
    url = get_authorization_url("zhib.wang09@gmail.com", None)
    print("url", url)
    
if __name__ == "__main__":
    main()