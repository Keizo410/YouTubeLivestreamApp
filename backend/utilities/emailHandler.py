
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os

class Email:
    """Creates a Email object"""
    def __init__(self):
        """
        Initialize the Email object.


        """
        self.sender = ""
        self.receiver = ""
        self.password = ""
        self.subject = ""
        self.body = ""
        self.msg = MIMEMultipart()
    
    def set_draft(self, subject, body):
        """
        Set email draft to the Email object.

        Parameters:
        subject - a string for email subject.
        body - a string for email content body.
        """
        self.subject = subject
        self.body = body
    
    def set_credentials(self, sender, password, receiver):
        """
        Set email credentials to the Email object.

        Parameters:
        sender - a string for sender email address.
        password - a string for password for logging in stmp server.
        receiver - a string for receiver email address.
        """
        self.sender = sender
        self.receiver = receiver
        self.password = password

    def get_draft(self):
        """
        Get method to retrieve draft info on the object.
        """
        return self.subject, self.body
    
    def get_credentials(self):
        """
        Get method to retrieve credentials info on the object.
        """
        return self.sender, self.receiver, self.password
    
    def write_email(self, csv_file_path='livechat_data.csv'):
        """
        A method to write email with draft and credentials, attach a data file to the Email object.

        Parameters:
        csv_file_path - file path for csv file that contains data
        """
        sender, receiver, _ = self.get_credentials()
        subject, body = self.get_draft()
        self.msg['From'] = sender
        self.msg['To'] = receiver
        self.msg['Subject'] = subject
        self.msg.attach(MIMEText(body, 'plain'))
        try:
            with open(csv_file_path, 'rb') as file:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(file.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(csv_file_path)}')
                self.msg.attach(part)
            return "File is attached correctly", 200
        except Exception as e:
            return f'Failed to attach file: {e}', 500

    def send_email(self):
        """
        A method to send email with SMTP.
        """
        sender, receiver, password = self.get_credentials()
        # subject, body = self.get_draft()
        try:
            s = smtplib.SMTP('smtp.gmail.com', 587)
            s.starttls()
            s.login(sender, password)
            s.sendmail(sender, receiver, self.msg.as_string())
            s.quit()
            return 'Mail has been sent successfully', 200
        except Exception as e:
            return f'Failed to send mail: {e}', 500
    
    