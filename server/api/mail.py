# this file contains the code for accessing the gmail api

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
import base64
from server.models.email import Email
from server.models.model import email_summarization_model
import jsonpickle
from bs4 import BeautifulSoup
import re



def get_messages(user_email: str, credentials: Credentials) -> list[Email]:
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
        results = (
            service.users().messages().list(userId=user_email, maxResults=5).execute()
        )
        messagesAPI = service.users().messages()
        messages = results.get("messages", [])
        emails = []
        if not messages:
            print("No messages found.")
            return
        for message in messages:
            m = messagesAPI.get(userId=user_email, id=message.get("id")).execute()
            snippet = m["snippet"]
            payload = m["payload"]
            email = parse_messages(payload)
            email.snippet = snippet
            email_summarization = email_summarization_model.infer(get_mail_plain_text(email))
            emails.append({"summarization": email_summarization, "email": get_mail_plain_text(email)})
        return emails
    except HttpError as error:
        print(f"An error occurred: {error}")


def parse_messages(messagePart):
    """messagePart is recursive structure hence we need to process the parts field recursively

    Args:
        messagePart (_type_): the payload of a email message

    Returns:
        A single email without the snippet because we are only parsing parts
    """
    mimeType = messagePart["mimeType"]
    subject = ""
    source = ""
    to = ""
    date = ""
    body = []

    # parse headers
    for h in messagePart["headers"]:
        header_name = h["name"]
        value = h["value"]
        if header_name == "Subject":
            subject = value
        elif header_name == "From":
            source = value
        elif header_name == "To":
            to = value
        elif header_name == "Date":
            date = value
    if "multipart/" in mimeType:
        # container MIME message part type
        # uses field parts[]
        # field body may be empty
        parts = messagePart["parts"]
        for p in parts:
            body.append(parse_messages(p))  # recursively add the payloads
    else:
        # non-container MIME message part type
        # uses body
        if "data" in messagePart["body"]:
            msg = base64.urlsafe_b64decode(messagePart["body"]["data"].encode()).decode(
                "utf-8", errors="replace"
            )
            body.append(msg)
    email = Email(
        date=date, mimeType=mimeType, source=source, to=to, subject=subject, body=body
    )
    return email

def get_mail_plain_text(email):
    """parse the email content to at least return a text/plain resul

    Args:
        email (Email): email representation

    Returns:
        str: text/plain of the email representation
    """
    text = ''
    text += 'Subject: ' + email.subject + '\n'
    text += 'Snipet: ' + email.snippet + '\n'
    text += 'From: ' + email.source + '\n'
    text += 'To: ' + email.to + '\n'
    body = ''
    if email.mimeType == 'text/html':
        soup = BeautifulSoup(email.body[0], 'html.parser')
        body = soup.get_text(separator=" ")
        re.sub(r'http[s]?://\S+', '', body)
    elif email.mimeType == 'text/plain':
        body = re.sub(r'http[s]?://\S+', '', email.body[0])
    else:
        for b in email.body:
            body = get_mail_plain_text(b)
    
    text += body + '\n'
    return text
                    