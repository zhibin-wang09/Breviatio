# this file contains the code for accessing the gmail api

from typing import List
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
import base64
from server.models.email import Email
from server.models.model import email_categorize
from server.models.part import Part
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
            
            # set up email object
            email : Email = extract_email_global_information(payload)
            body = parse_messages(email.mimeType, payload['parts'])
            email.body = body
            email.snippet = snippet
            
            # email now contains all of its payloads
            # we want to only use the simplest form for classification because it reduces noise
            email_content_for_classification = select_simplest_email_content(email.body)
            
            plain_text_email = get_mail_plain_text(email_content_for_classification)
            category = email_categorize.infer(plain_text_email)
            emails.append({"category": category, "email": email.subject})
        return emails
    except HttpError as error:
        print(f"An error occurred: {error}")
        
def select_simplest_email_content(body: List[Part]) -> Part:
    simplest_body = None
    for m in body:
        if m.mimeType == 'text/plain':
            return m
        else:
            simplest_body = m
    
    return simplest_body
        
def extract_email_global_information(message):
    """extract global information like sender, receiver, date, subject, etc only

    Args:
        message (json): contains the body and global information
    """
    mimeType = message["mimeType"]
    subject = ""
    source = ""
    to = ""
    date = ""
    body = []
    
    # parse headers
    for h in message["headers"]:
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
            
    email = Email(
        date=date, mimeType=mimeType, source=source, to=to, subject=subject, body=[]
    )
    return email

def parse_messages(mimeType, parts) -> List[Part]:
    """messagePart is recursive structure hence we need to process the parts field recursively

    Args:
        messagePart (_type_): the payload of a email message

    Returns:
        A single email without the snippet because we are only parsing parts
    """
    body : List[Part] = []
    if "multipart/" in mimeType:
        # container MIME message part type
        # uses field parts[]
        # field body may be empty
        
        for p in parts:
            mimeType = p['mimeType']
            body.append(parse_messages(mimeType,p))  # recursively add the payloads
    else:
        # non-container MIME message part type
        # uses body
        if "data" in parts["body"]:
            msg = base64.urlsafe_b64decode(parts["body"]["data"].encode()).decode(
                "utf-8", errors="replace"
            )
            body.append(Part(mimeType=mimeType, body=msg))

    return body

def get_mail_plain_text(email):
    """parse the email content to at least return a text/plain result

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
    # with open('test.json', 'a') as file:
    #     file.write(text)
    #     file.write('\n')
    
    return text
                    