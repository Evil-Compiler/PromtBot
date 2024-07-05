# text_submission.py

import os
from cryptography.fernet import Fernet
import random

class TextSubmission:
    def __init__(self, file_name='submissions.txt', key_file='secret.key'):
        """Initialize the submission system with a file name and encryption key."""
        self.file_name = file_name
        self.key_file = key_file
        self.load_key()
        self.load_submissions()

    def load_key(self):
        """Load or generate an encryption key."""
        if os.path.exists(self.key_file):
            with open(self.key_file, 'rb') as file:
                self.key = file.read()
        else:
            self.key = Fernet.generate_key()
            with open(self.key_file, 'wb') as file:
                file.write(self.key)
        self.cipher = Fernet(self.key)

    def encrypt(self, text):
        """Encrypt a string using Fernet."""
        return self.cipher.encrypt(text.encode()).decode()

    def decrypt(self, text):
        """Decrypt a string using Fernet."""
        return self.cipher.decrypt(text.encode()).decode()

    def escape_newlines(self, text):
        """Escape newlines in the text."""
        return text.replace('\n', '\\n')

    def unescape_newlines(self, text):
        """Unescape newlines in the text."""
        return text.replace('\\n', '\n')

    def load_submissions(self):
        """Load submissions from the file."""
        if os.path.exists(self.file_name):
            with open(self.file_name, 'r') as file:
                self.submissions = [line.strip().split('::', 2) for line in file]
                self.submissions = [(self.decrypt(user), category, self.unescape_newlines(text)) for user, category, text in self.submissions]
        else:
            self.submissions = []

    def save_submissions(self):
        """Save submissions to the file."""
        with open(self.file_name, 'w') as file:
            for submission in self.submissions:
                encrypted_user = self.encrypt(submission[0])
                escaped_text = self.escape_newlines(submission[2])
                file.write(f"{encrypted_user}::{submission[1]}::{escaped_text}\n")

    def submit_text(self, user, category, text):
        """Add a new text submission with a category and save to file if it doesn't already exist."""
        if text not in (submission[2] for submission in self.submissions):
            submission = (user, category, text)
            self.submissions.append(submission)
            self.save_submissions()
            return True
        return False

    def delete_text(self, user, text, admin=False):
        """Delete a text submission and save to file."""
        submission = [(u, c, t) for u, c, t in self.submissions if t == text and (admin or u == user)]
        if submission:
            self.submissions = [s for s in self.submissions if s not in submission]
            self.save_submissions()
            return True
        return False

    def get_random_submission(self, category=None):
        """Return a random text submission from the list, optionally filtered by category."""
        submissions = [s for s in self.submissions if category is None or s[1] == category]
        if submissions:
            return random.choice(submissions)[2]
        else:
            return "No submissions available."

    def get_all_submissions(self, category=None):
        """Return all text submissions from the list, optionally filtered by category."""
        submissions = [s for s in self.submissions if category is None or s[1] == category]
        if submissions:
            separator = "\n----------------------\n"
            return '\n'.join(f"Category: {submission[1]} - Text: {submission[2]} {separator}" for submission in submissions)
        else:
            return "No submissions available."  