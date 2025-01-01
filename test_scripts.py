"""
This script handles fetching emails, analyzing sentiment, and saving results to a CSV file.
"""

# Standard Library Imports
import time
import logging
import traceback

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("test_scripts.log"),
        logging.StreamHandler()
    ]
)

# Measure time for imports
start_imports = time.time()

# Measure time for standard library imports
start_logging = time.time()
try:
    import logging
    logging.info("Successfully imported logging in %.2f seconds.", time.time() - start_logging)
except Exception as e:
    logging.error("Error importing logging: %s", e)
    raise

start_traceback = time.time()
try:
    import traceback
    logging.info("Successfully imported traceback in %.2f seconds.", time.time() - start_traceback)
except Exception as e:
    logging.error("Error importing traceback: %s", e)
    raise

# Measure time for third-party imports
start_pandas = time.time()
try:
    import pandas as pd
    logging.info("Successfully imported pandas in %.2f seconds.", time.time() - start_pandas)
except Exception as e:
    logging.error("Error importing pandas: %s", e)
    raise

# Measure time for local imports
start_authenticate = time.time()
try:
    from auth_utils import authenticate
    logging.info("Successfully imported authenticate from auth_utils in %.2f seconds.", time.time() - start_authenticate)
except ImportError as e:
    logging.error("ImportError importing authenticate: %s", e)
    traceback.print_exc()

start_fetch_emails = time.time()
try:
    from fetch_emails import fetch_emails
    logging.info("Successfully imported fetch_emails in %.2f seconds.", time.time() - start_fetch_emails)
except Exception as e:
    logging.error("Error importing fetch_emails: %s", e)
    raise

start_analyze_sentiment = time.time()
try:
    from analyze_sentiment import analyze_sentiment
    logging.info("Successfully imported analyze_sentiment in %.2f seconds.", time.time() - start_analyze_sentiment)
except Exception as e:
    logging.error("Error importing analyze_sentiment: %s", e)
    raise

logging.info("Total time for all imports: %.2f seconds.", time.time() - start_imports)




# Updated save_to_csv function to include truncation
def save_to_csv(emails):
    """
    Saves a list of email dictionaries to a CSV file, truncating long content.

    Args:
        emails (list): A list of email dictionaries to be saved.
    """
    try:
        logging.info("Emails content: %s", emails[:5])  # Log first 5 emails for debugging
        if not isinstance(emails, list) or not all(isinstance(email, dict) for email in emails):
            raise ValueError("Invalid format for emails. Expected a list of dictionaries.")

        # Apply truncation to email content if required
        for email in emails:
            if 'body' in email:
                email['body'] = truncate_text(email['body'])

        # Convert the list of email dictionaries to a DataFrame
        df = pd.DataFrame(emails)
        df.to_csv("emails_with_sentiment.csv", index=False)
        logging.info("Emails saved to emails_with_sentiment.csv")
    except pd.errors.EmptyDataError:
        logging.error("No data to save to CSV.")
    except pd.errors.ParserError:
        logging.error("Error parsing data to CSV.")
    except ValueError as e:
        logging.error("ValueError occurred: %s", e)
    except Exception as e:
        logging.error("Unexpected error saving emails to CSV: %s", e)
        logging.error(traceback.format_exc())

# Example usage of the truncate_text function in test_scripts
def test_scripts():
    """
    Main function to authenticate, fetch emails with a query, analyze sentiment, and save results to a CSV file.
    """
    try:
        logging.info("Starting test_scripts.")

        # Measure authentication time
        start_auth = time.time()
        creds = authenticate()
        logging.info("Authentication completed in %.2f seconds.", time.time() - start_auth)

        # Define query and measure fetching time
        query = '''(category:updates (travel OR reservation OR confirmation OR itinerary OR booking)) after:2023/12/31'''
        start_fetch = time.time()
        emails = fetch_emails(creds, query)
        logging.info("Fetched %d emails in %.2f seconds.", len(emails), time.time() - start_fetch)

        # Measure sentiment analysis time
        start_analysis = time.time()
        analyzed_emails = analyze_sentiment(emails)
        logging.info("Sentiment analysis completed in %.2f seconds.", time.time() - start_analysis)

        # Apply truncation here if needed for other fields (optional)
        for email in analyzed_emails:
            if 'body' in email:
                email['body'] = truncate_text(email['body'])

        # Measure saving to CSV time
        start_save = time.time()
        save_to_csv(analyzed_emails)
        logging.info("Saving to CSV completed in %.2f seconds.", time.time() - start_save)

    except Exception as e:
        logging.error("Error during test_scripts: %s", e)
        logging.error(traceback.format_exc())

if __name__ == "__main__":
    test_scripts()