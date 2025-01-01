import logging
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from base64 import urlsafe_b64decode

# fetch_emails.py
def fetch_emails(creds, query=None):
    """
    Fetches emails from the Gmail API based on the provided query.

    Args:
        creds: Credentials object for Gmail API.
        query (str): Gmail query string to filter emails.

    Returns:
        list: List of fetched email dictionaries.
    """
    try:
        service = build('gmail', 'v1', credentials=creds)
        logging.info("Fetching emails with query: %s", query)

        results = service.users().messages().list(userId='me', q=query).execute()
        messages = results.get('messages', [])

        emails = []
        for message in messages:
            msg = service.users().messages().get(userId='me', id=message['id']).execute()
            emails.append({
                'id': msg['id'],
                'snippet': msg['snippet'],
                'payload': msg.get('payload', {}),
            })

        logging.info("Fetched %d emails.", len(emails))
        return emails
    except Exception as e:
        logging.error("Error fetching emails: %s", e)
        logging.error(traceback.format_exc())
        raise