# this file contains the code for accessing the gmail api

import json
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import base64
import jsonpickle

from server.models.email import Email


def getMessages(user_email: str, credentials) -> list[Email]:
  """
  Return user messages
  """
  
  
  # gmail messages is of type users.message
  # this object have payload of type users.messageparts
  # users.messageparts have a field called mimeType this tells us what type of
  # content this email contains. (It is a two part identifier <file format>/<content format>)
  # users.messagrParts content changes change on the type

  # users.messageParts does not have field parts[] when mime type is text/plain and 
  # have field parts[] when type is multipart/*

  # when messageParts is multipart/* use parts[] when messageParts is text/plain use body
  
  try:
    # Call the Gmail API
    service = build("gmail", "v1", credentials=credentials)
    results = service.users().messages().list(userId=user_email).execute()
    messagesAPI = service.users().messages()
    messages = results.get("messages", [])
    emails = []
    if not messages:
      print("No messages found.")
      return
    for message in messages:
        m = messagesAPI.get(userId=user_email, id=message.get("id")).execute()
        snippet = m['snippet']
        payload = m['payload']
        email = parseMessages(payload)
        email.snippet = snippet
        emails.append(jsonpickle.dumps(email))
    return emails
  except HttpError as error:
    print(f"An error occurred: {error}")
    
  
def parseMessages(messagePart):
  mimeType = messagePart['mimeType']
  subject = ''
  source = ''
  to = ''
  date = ''
  body = []
  
  # parse headers
  for h in messagePart['headers']:
    header_name = h['name']
    value = h['value']
    if header_name == 'Subject':
      subject = value
    elif header_name == 'From':
      source = value
    elif header_name == 'To':
      to = value
    elif header_name == 'Date': 
      date = value
  if 'multipart/' in mimeType:
    # container MIME message part type
    # uses field parts[]
    # field body may be empty
    parts = messagePart['parts']
    for p in parts:
      body.append(parseMessages(p)) # recursively add the payloads
  else:
    # non-container MIME message part type
    # uses body
    if 'data' in messagePart['body']:
      msg = base64.urlsafe_b64decode(messagePart['body']['data'].encode()).decode('utf-8', errors='replace')
      body.append(msg)
  email = Email(date=date, mimeType=mimeType, source=source, to=to, subject=subject, body=body)
  return email;