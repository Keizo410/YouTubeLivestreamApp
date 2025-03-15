import pytest
from utilities.emailHandler import Email
from unittest.mock import patch, MagicMock

@pytest.fixture
def empty_email():
    return Email()

def test_drafting(empty_email):
    """Test set/get drafting functions"""
    subject = "Test subject"
    body = "Test body"
    empty_email.set_draft(subject, body)
    draft_subject, draft_body = empty_email.get_draft()
    assert draft_subject == subject
    assert draft_body == body 

def test_credentials(empty_email):
    """Test set/get credentials functions"""
    sender = "test"
    password = "test"
    receiver = "test"
    empty_email.set_credentials(sender, receiver, password)
    cred_sender, cred_receiver, cred_password = empty_email.get_credentials()
    assert cred_sender == sender
    assert cred_receiver == receiver
    assert cred_password == password


def test_write_email_success(empty_email):
    """Test write email function successful"""
    sender = "test"
    password = "test"
    receiver = "test"
    empty_email.set_credentials(sender, receiver, password)
    subject = "Test subject"
    body = "Test body"
    empty_email.set_draft(subject, body)
    message, status = empty_email.write_email()
    assert status == 200

def test_send_email_failure(empty_email):
    """Test email sending failure by simulating an exception during login."""
    empty_email.set_credentials("test_sender@example.com", "password", "test_receiver@example.com")
    empty_email.set_draft("Test Subject", "Test Body")

    with patch("smtplib.SMTP") as mock_smtp:
        mock_smtp_instance = MagicMock()
        mock_smtp.return_value = mock_smtp_instance

        mock_smtp_instance.login.side_effect = Exception("SMTP login failed")

        response = empty_email.send_email()

        assert response[0].startswith("Failed to send mail: SMTP login failed")
        assert response[1] == 500

def test_send_email_success(empty_email):
    """Test successful email sending using a mock SMTP server."""
    empty_email.set_credentials("test_sender@example.com", "password", "test_receiver@example.com")
    empty_email.set_draft("Test Subject", "Test Body")

    with patch("smtplib.SMTP") as mock_smtp:
        mock_smtp_instance = MagicMock()
        mock_smtp.return_value = mock_smtp_instance

        response = empty_email.send_email()

        assert response == ("Mail has been sent successfully", 200)