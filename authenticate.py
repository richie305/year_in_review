# Description: This script authenticates the user and returns the credentials object.

# Standard library imports
import logging
import os
import pickle
import traceback

# Third-party imports
import pandas as pd
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Local application imports
from analyze_sentiment import analyze_sentiment

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("test_scripts.log"),  # Log messages to a file
        logging.StreamHandler()  # Also print messages to the console
    ]
)
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def authenticate():
    try:
        creds = None
        # Check if token exists
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
                logging.info("Loaded existing credentials.")

        # If there are no valid credentials, request a new login
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
                logging.info("Refreshed expired credentials.")
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
                logging.info("New credentials generated.")

            # Save credentials for future use
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
                logging.info("Saved credentials to token.pickle.")

        return creds
    except Exception as e:
        logging.error(f"Authentication failed: {e}")
        raise
