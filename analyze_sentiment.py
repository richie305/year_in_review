import logging
import os
import time
from openai import OpenAI

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("test_scripts.log"),  # Log messages to a file
        logging.StreamHandler()  # Also print messages to the console
    ]
)

# Set your OpenAI API key (ensure this is handled securely in production environments)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is not set in the environment variables")

print(f"Your API key is: {OPENAI_API_KEY}")
MAX_CONTENT_LENGTH = 3000  # Adjust based on OpenAI's token limits

def analyze_sentiment(emails):
    """
    Analyzes the sentiment of a list of emails using OpenAI's GPT model.

    Args:
        emails (list): A list of email dictionaries with 'id' and 'snippet' or 'content' keys.

    Returns:
        list: A list of dictionaries with 'id', 'content', and 'sentiment' keys.
    """
    processed_emails = []
    for email in emails:
        try:
            # Extract the email content
            email_content = email.get('snippet', '') or email.get('content', '')

            # Validate and preprocess the content
            if isinstance(email_content, list):
                email_content = " ".join(email_content)
            elif not isinstance(email_content, str):
                logging.warning(f"Skipping email {email.get('id', 'unknown')} due to invalid content type.")
                continue

            # Truncate the content to fit within token limits
            email_content = email_content.strip()
            if len(email_content) > MAX_CONTENT_LENGTH:
                email_content = email_content[:MAX_CONTENT_LENGTH]

            # Perform sentiment analysis using the updated API syntax
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that analyzes email sentiment."},
                    {"role": "user", "content": f"Analyze the sentiment of this email: {email_content}"}
                ],
                max_tokens=50
            )
            sentiment = response.choices[0].message.content.strip()

            # Append the processed email with sentiment
            processed_emails.append({
                'id': email.get('id', 'unknown'),
                'content': email_content,
                'sentiment': sentiment
            })

        except Exception as e:
            logging.error(f"Error analyzing email {email.get('id', 'unknown')}: {e}")
            continue

    return processed_emails

def extract_body_from_payload(payload):
    """
    Extracts plain text or HTML content from the email payload.

    Args:
        payload (dict): The payload field from an email entry.

    Returns:
        str: Extracted text from the email body or parts.
    """
    try:
        if not isinstance(payload, dict):
            return ""

        # Look for parts containing the email body
        parts = payload.get('parts', [])
        for part in parts:
            if part.get('mimeType') == "text/plain":
                return part.get('body', {}).get('data', '')  # Extract plain text
            elif part.get('mimeType') == "text/html":
                html_content = part.get('body', {}).get('data', '')
                return extract_text_from_html(html_content)

        return ""
    except Exception as e:
        logging.error("Error extracting body from payload: %s", e)
        return ""


def extract_text_from_html(html_content):
    """
    Strips HTML tags from a given string.

    Args:
        html_content (str): The HTML content to process.

    Returns:
        str: Plain text extracted from HTML.
    """
    try:
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        return soup.get_text()
    except ImportError:
        logging.warning("BeautifulSoup not installed. Returning raw HTML.")
        return html_content