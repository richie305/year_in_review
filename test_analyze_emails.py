import unittest
from analyze_emails import generate_keywords, analyze_emails

class TestAnalyzeEmails(unittest.TestCase):

    def test_generate_keywords(self):
        email_body = "Your Delta flight to Puerto Rico is confirmed for February 14, 2025."
        expected_keywords = ["Delta", "flight", "Puerto Rico", "February 14, 2025"]
        keywords = generate_keywords(email_body)
        self.assertTrue(all(keyword in keywords for keyword in expected_keywords))

    def test_analyze_emails(self):
        test_emails = [
            {"subject": "Flight Confirmation", "body": "Your Delta flight to Puerto Rico is confirmed for February 14, 2025."},
            {"subject": "Hotel Reservation", "body": "Your stay at the Hyatt Regency Pittsburgh is confirmed for February 13, 2025."},
        ]
        analyzed_emails = analyze_emails(test_emails)

        # Check that all emails have 'keywords'
        for email in analyzed_emails:
            self.assertIn("keywords", email)
            self.assertTrue(len(email["keywords"]) > 0)

if __name__ == "__main__":
    unittest.main()