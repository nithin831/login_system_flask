from flask_mail import Message
from config import mail

# send an verification link to activate an account
def send_verification_email(email, link):
    subject = "Verify Your Email Address"
    body = f"""
    Hi,

    Thank you for signing up with us! To complete your registration, please verify your email address by clicking the link below:

    {link}

    This link is valid for 5 minutes. If you did not sign up for an account, you can safely ignore this email.

    Thank you,
    YourApp Team
    """
    msg = Message(subject, recipients=[email], body=body)
    mail.send(msg)

# Send a password reset email with the reset link
def send_reset_password_email(email, reset_link):
    subject = "Password Reset Request"
    body = f"""
    Hi,

    We received a request to reset your password. Please click the link below to reset your password:

    {reset_link}

    If you did not request a password reset, please ignore this email.

    This link is valid for 5 minutes.

    Thank you,
    YourApp Team
    """
    msg = Message(subject, recipients=[email], body=body)
    mail.send(msg)
