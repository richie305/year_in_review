import logging
import json
from tqdm import tqdm  # Progress bar library
from openai import OpenAI

client = OpenAI(api_key=openai_api_key)

# Configure logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

# Load API key
with open("credentials.json", "r") as cred_file:
    credentials = json.load(cred_file)
openai_api_key = credentials.get("openai_api_key")

def generate_keywords(email_content: str) -> list:
    """
    Generate travel-related keywords from email content using GPT.

    Args:
        email_content (str): The raw content of the email.

    Returns:
        list: A list of descriptive keywords related to travel.
    """
    from openai import OpenAI

    client = OpenAI(api_key=openai_api_key)

    try:
        response = client.chat.completions.create(model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that extracts travel-related keywords from emails."},
            {"role": "user", "content": f"Extract travel-related keywords from this email: {email_content}"}
        ])

        # Log raw response for debugging
        logging.debug(f"OpenAI Response: {response}")

        # Extract and return keywords
        keywords = response.choices[0].message.content.strip().split(", ")
        logging.info(f"Keywords generated: {keywords}")
        return keywords

    except openai.OpenAIError as e:  # Corrected exception handling
        logging.error(f"OpenAI API error: {e}")
        return []
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return [] # Return an empty list on error

def analyze_emails(emails: list) -> list:
    """
    Analyze a list of emails and assign descriptive, travel-related keywords to each.

    Args:
        emails (list): A list of emails where each email contains 'subject' and 'body'.

    Returns:
        list: A list of emails with added 'keywords'.
    """
    logging.info("Starting email analysis.")
    analyzed_emails = []

    # Initialize progress bar with tqdm
    for email in tqdm(emails, desc="Processing Emails", unit="email"):
        try:
            keywords = generate_keywords(email.get("body", ""))
            email_with_keywords = {
                "subject": email.get("subject", ""),
                "body": email.get("body", ""),
                "keywords": keywords
            }
            analyzed_emails.append(email_with_keywords)
            logging.info(f"Processed email: {email_with_keywords['subject']}")
        except Exception as e:
            logging.error(f"Error analyzing email: {e}")

    return analyzed_emails

if __name__ == "__main__":
    # Sample emails for testing
    test_emails = [
        {"subject": "Flight Confirmation", "body": "Your Delta flight to Puerto Rico is confirmed for February 14, 2025."},
        {"subject": "Hotel Reservation", "body": "Your stay at the Hyatt Regency Pittsburgh is confirmed for February 13, 2025."},
    ]

    # Run the analysis
    analyzed_data = analyze_emails(test_emails)

    # Log the analyzed data
    logging.info("Analyzed email data:")
    for email in analyzed_data:
        logging.info(email)