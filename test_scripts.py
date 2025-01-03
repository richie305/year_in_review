import logging
import time
from fetch_emails import fetch_emails
from analyze_emails import analyze_emails

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def main():
    """
    Main function to fetch emails, analyze them for travel-related keywords, and save results.
    """
    logging.info("Starting email processing pipeline.")

    # Step 1: Fetch Emails
    start_fetch = time.time()
    try:
        emails = fetch_emails()
        logging.info(f"Fetched {len(emails)} emails in {time.time() - start_fetch:.2f} seconds.")
    except Exception as e:
        logging.error(f"Error fetching emails: {e}")
        return

    # Step 2: Analyze Emails
    start_analyze = time.time()
    try:
        analyzed_emails = analyze_emails(emails)
        logging.info(f"Analyzed emails in {time.time() - start_analyze:.2f} seconds.")
    except Exception as e:
        logging.error(f"Error analyzing emails: {e}")
        return

    # Step 3: Save Results to a Log File (or Database/JSON as needed)
    try:
        with open("processed_emails.json", "w") as outfile:
            import json
            json.dump(analyzed_emails, outfile, indent=4)
        logging.info("Saved analyzed emails to processed_emails.json.")
    except Exception as e:
        logging.error(f"Error saving analyzed emails: {e}")

if __name__ == "__main__":
    main()