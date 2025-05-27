# this file contains the code for accessing the gmail api

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError



# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def getMessages(user_email: str, credentials):
  """Shows basic usage of the Gmail API.
  Return user messages
  """
  
  try:
    # Call the Gmail API
    service = build("gmail", "v1", credentials=credentials)
    results = service.users().messages().list(userId=user_email).execute()
    messagesAPI = service.users().messages()
    messages = results.get("messages", [])
    ms = []
    if not messages:
      print("No messages found.")
      return
    for message in messages:
        m = messagesAPI.get(userId=user_email, id=message.get("id")).execute()
        ms.append(m)
    return ms
  except HttpError as error:
    print(f"An error occurred: {error}")