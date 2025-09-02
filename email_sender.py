import smtplib
import csv
import json
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
import os
from typing import List, Dict, Optional
import time
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('email_log.txt'),
        logging.StreamHandler()
    ]
)

class EmailSender:
    def __init__(self):
        """Initialize EmailSender with configuration from environment variables."""
        self.config = self.load_config()
        self.smtp_server = None
        
    def load_config(self) -> Dict:
        """Load email configuration from environment variables."""
        # Load environment variables from .env file
        load_dotenv(override=True)
        
        # Get configuration from environment variables
        config = {
            'email': os.getenv('GMAIL_EMAIL'),
            'password': os.getenv('GMAIL_PASSWORD'),
            'smtp_server': os.getenv('SMTP_SERVER', 'smtp.gmail.com'),
            'smtp_port': int(os.getenv('SMTP_PORT', '587')),
            'sender_name': os.getenv('SENDER_NAME', 'Dummy Sender')
        }
        
        # Validate required configuration
        if not config['email'] or not config['password']:
            logging.error("Missing required environment variables: GMAIL_EMAIL and GMAIL_PASSWORD must be set")
            raise ValueError("Missing required environment variables. Please check your .env file.")
            
        return config
    
    def connect_to_gmail(self) -> bool:
        """Establish connection to Gmail SMTP server."""
        try:
            self.smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
            self.smtp_server.starttls()  # Enable encryption
            self.smtp_server.login(self.config['email'], self.config['password'])
            logging.info("Successfully connected to Gmail SMTP server")
            return True
        except Exception as e:
            logging.error(f"Failed to connect to Gmail: {str(e)}")
            return False
    
    def load_recipients_from_csv(self, csv_file: str) -> List[Dict]:
        """Load recipient list from CSV file."""
        recipients = []
        try:
            with open(csv_file, 'r', newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    recipients.append(row)
            logging.info(f"Loaded {len(recipients)} recipients from {csv_file}")
            return recipients
        except FileNotFoundError:
            logging.error(f"Recipients file {csv_file} not found!")
            return []
        except Exception as e:
            logging.error(f"Error loading recipients: {str(e)}")
            return []
    
    def load_email_template(self, template_file: str) -> Dict:
        """Load email template from file."""
        try:
            with open(template_file, 'r', encoding='utf-8') as f:
                template = json.load(f)
            return template
        except FileNotFoundError:
            logging.error(f"Template file {template_file} not found!")
            return {}
        except Exception as e:
            logging.error(f"Error loading template: {str(e)}")
            return {}
    
    def personalize_message(self, template: str, recipient: Dict) -> str:
        """Personalize email message with recipient data."""
        personalized = template
        for key, value in recipient.items():
            placeholder = f"{{{key}}}"
            personalized = personalized.replace(placeholder, str(value))
        # Replace {Sender_Name} with config sender_name
        if '{Sender_Name}' in personalized:
            personalized = personalized.replace('{Sender_Name}', self.config.get('sender_name', 'MailWhale Sender'))
        return personalized
    
    def create_email(self, recipient: Dict, template: Dict, attachments: Optional[List[str]] = None) -> MIMEMultipart:
        """Create email message."""
        msg = MIMEMultipart()
        msg['From'] = self.config['email']
        msg['To'] = recipient['Receiver_Mail']
        msg['Subject'] = self.personalize_message(template['subject'], recipient)
        
        # Create email body
        body = self.personalize_message(template['body'], recipient)
        msg.attach(MIMEText(body, 'plain'))
        
        # Add attachments if provided
        if attachments:
            for file_path in attachments:
                if os.path.isfile(file_path):
                    with open(file_path, "rb") as attachment:
                        part = MIMEBase('application', 'octet-stream')
                        part.set_payload(attachment.read())
                    
                    encoders.encode_base64(part)
                    part.add_header(
                        'Content-Disposition',
                        f'attachment; filename= {os.path.basename(file_path)}'
                    )
                    msg.attach(part)
        
        return msg
    
    def send_bulk_emails(self, recipients_file: str, template_file: str, 
                        attachments: Optional[List[str]] = None, 
                        delay_seconds: int = 1) -> Dict:
        """Send bulk emails to all recipients."""
        # Load data
        recipients = self.load_recipients_from_csv(recipients_file)
        template = self.load_email_template(template_file)
        
        if not recipients or not template:
            return {"success": 0, "failed": 0, "errors": ["Failed to load recipients or template"]}
        
        # Connect to Gmail
        if not self.connect_to_gmail():
            return {"success": 0, "failed": 0, "errors": ["Failed to connect to Gmail"]}
        
        success_count = 0
        failed_count = 0
        errors = []
        
        try:
            for i, recipient in enumerate(recipients, 1):
                try:
                    # Create and send email
                    msg = self.create_email(recipient, template, attachments)
                    self.smtp_server.send_message(msg)
                    
                    success_count += 1
                    logging.info(f"Email {i}/{len(recipients)} sent successfully to {recipient['Receiver_Mail']}")
                    
                    # Add delay to avoid being flagged as spam
                    if delay_seconds > 0 and i < len(recipients):
                        time.sleep(delay_seconds)
                        
                except Exception as e:
                    failed_count += 1
                    error_msg = f"Failed to send email to {recipient.get('Receiver_Mail', 'unknown')}: {str(e)}"
                    errors.append(error_msg)
                    logging.error(error_msg)
                    
        finally:
            # Close connection
            if self.smtp_server:
                self.smtp_server.quit()
                logging.info("SMTP connection closed")
        
        return {
            "success": success_count,
            "failed": failed_count,
            "errors": errors
        }
    
    def send_single_email(self, recipient_email: str, subject: str, body: str, 
                         attachments: Optional[List[str]] = None) -> bool:
        """Send a single email."""
        if not self.connect_to_gmail():
            return False
        
        try:
            msg = MIMEMultipart()
            msg['From'] = self.config['email']
            msg['To'] = recipient_email
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))
            
            # Add attachments if provided
            if attachments:
                for file_path in attachments:
                    if os.path.isfile(file_path):
                        with open(file_path, "rb") as attachment:
                            part = MIMEBase('application', 'octet-stream')
                            part.set_payload(attachment.read())
                        
                        encoders.encode_base64(part)
                        part.add_header(
                            'Content-Disposition',
                            f'attachment; filename= {os.path.basename(file_path)}'
                        )
                        msg.attach(part)
            
            self.smtp_server.send_message(msg)
            logging.info(f"Email sent successfully to {recipient_email}")
            return True
            
        except Exception as e:
            logging.error(f"Failed to send email to {recipient_email}: {str(e)}")
            return False
        finally:
            if self.smtp_server:
                self.smtp_server.quit()

def main():
    """Example usage of EmailSender."""
    try:
        # Initialize email sender
        sender = EmailSender()
        
        # Example 1: Send bulk emails
        print("Sending bulk emails...")
        result = sender.send_bulk_emails(
            recipients_file='recipients.csv',
            template_file='email_template.json',
            delay_seconds=2  # 2 second delay between emails
        )
        
        print(f"Bulk email results:")
        print(f"Success: {result['success']}")
        print(f"Failed: {result['failed']}")
        if result['errors']:
            print("Errors:")
            for error in result['errors']:
                print(f"  - {error}")
        
        # Example 2: Send single email
        # sender.send_single_email(
        #     recipient_email="example@example.com",
        #     subject="Test Email",
        #     body="This is a test email sent from Python!"
        # )
        
    except Exception as e:
        logging.error(f"Application error: {str(e)}")

if __name__ == "__main__":
    main()
