# this file contains the code for accessing the gmail api

from typing import List
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
import base64
from server.models.email import Email
from server.models.part import Part
import html2text



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
            service.users().messages().list(userId=user_email, maxResults=500).execute()
        )
        messagesAPI = service.users().messages()
        messages = results.get("messages", [])
        emails = []
        if not messages:
            print("No messages found.")
            return
        
        count = 0
        for message in messages:
            email_json = messagesAPI.get(userId=user_email, id=message.get("id")).execute()

            # set up email object
            email : Email = parse_email(email_json)
            
            # email now contains all of its payloads
            # we want to only use the simplest form for classification because it reduces noise
            email_content_for_classification = select_simplest_email_content(email.body)
             
            plain_text_email = get_email_plain_text(email, email_content_for_classification)
            with open(f'training/emails/email_{count}.json', "+a") as file:
                file.write(plain_text_email)
                count += 1
            # category = email_categorize.infer(plain_text_email)
            
            # emails.append({"category": category, "email": email.subject})
        return emails
    except HttpError as error:
        print(f"An error occurred: {error}")
        
def select_simplest_email_content(body: List[Part]) -> Part:
    """find text/plain from multi part or if text/plain doesn't exist, find text/html 

    Args:
        body (List[Part]): _description_

    Returns:
        Part: _description_
    """

    text_plain = None
    text_html = None
    fall_back = None
    for m in body:
        if m.mimeType == 'text/plain':
            text_plain = m
        elif m.mimeType == 'text/html':
            text_html = m
        elif 'multipart/' in m.mimeType: # is multi part
            fall_back = select_simplest_email_content(m)
    
    if text_plain:
        return text_plain
    elif text_html:
        return text_html
    else:
        return fall_back
        
def parse_email(email_json) -> Email:
    """turn json response object email into our representation of Email

    Args:
        email (json): contains the body and global information
        
    Returns:
        Email object
    """
    payload = email_json['payload']
    mimeType = payload["mimeType"]
    subject = ""
    source = ""
    to = ""
    date = ""
    snippet = email_json['snippet']
    
    # parse headers
    for h in payload["headers"]:
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
        date=date, mimeType=mimeType, source=source, to=to, subject=subject, body=parse_email_body(mimeType=mimeType, payload=payload), snippet=snippet
    )
    
    return email

def parse_email_body(mimeType, payload) -> List[Part]:
    """messagePart is recursive structure hence we need to process the parts field recursively

    Args:
        mimeType (str): type of the email
        payload (str): body of the email, can be of different types depending on mimeType

    Returns:
        A single email without the snippet because we are only parsing parts
    """
    body : List[Part] = []
    if "multipart/" in mimeType:
        # container MIME message part type
        # uses field parts[]
        # field body may be empty
        parts = payload['parts']
        for p in parts:
            mimeType = p['mimeType']
            body.extend(parse_email_body(mimeType,p))  # recursively add the payloads
    else:
        # non-container MIME message part type
        # uses body
        if "data" in payload["body"]:
            msg = base64.urlsafe_b64decode(payload["body"]["data"].encode()).decode(
                "utf-8", errors="replace"
            )
            body.append(Part(mimeType=mimeType, body=msg))

    return body

def get_email_plain_text(email : Email, part : Part):
    """parse the email content to at least return a text/plain result

    Args:
        email (Email): email representation that holds the meta data
        part (Part): the body of the email

    Returns:
        str: text/plain of the email representation
    """
    text = ''
    text += 'Subject: ' + email.subject + '\n'
    text += 'Snipet: ' + email.snippet + '\n'
    text += 'From: ' + email.source + '\n'
    text += 'To: ' + email.to + '\n'
    body = ''
    if part.mimeType == 'text/html':
        body = html2text.html2text(part.body)
        print(email.subject, 'html')
    elif part.mimeType == 'text/plain':
        # body = re.sub(r'http[s]?://\S+', '', part.body)
        body = part.body
        print(email.subject, 'text')
    
    text += body + '\n'
    return text
                    