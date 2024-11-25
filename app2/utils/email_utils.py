from flask_mail import Message
from config import mail

def send_verification_email(email, link):
    msg = Message("Email Verification", recipients=[email])
    msg.body = f"Please verify your email by clicking the following link: {link} The link will expire in 5 minutes."
    mail.send(msg)
