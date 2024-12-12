from flask_mail import Message
from config import mail
from datetime import datetime, timedelta

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

def send_create_user_email_from_admin(user_email, user_name, new_password):
    """
    Sends an email to the user notifying them about their password change.
    """
    # Email content
    subject = "Your account created by admin"
    expiration_date = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
    body = f"""
    Hi {user_name},

    Your account has been created successfully by admin. For security reasons, please change your password before {expiration_date}.
    
    Your  mail id : {user_email}
    Your temporary password is: {new_password}

    To update your password, please log in to your account with the given credentials and navigate to the 'Change Password' section.

    If you did not request this change, please contact support immediately.

    Regards,
    Your Company Support Team
    """
    msg = Message(subject, recipients=[user_email], body=body)
    mail.send(msg)

def send_account_update_email(user_email):
    """
    Sends an email to the user notifying them about the successful update of their account details.
    """
    # Email content
    subject = "Your Account Details Have Been Successfully Updated"
    body = f"""
    Hi Sir/Madam,

    We're happy to inform you that your account details have been successfully updated.

    If you did not make these changes or have any concerns, please contact our support team immediately.

    Regards,
    Your Company Support Team
    """
    msg = Message(subject, recipients=[user_email], body=body)
    mail.send(msg)

def send_login_link(email, login_link):
    subject = "Secure Login Link for Your Account"
    body = f"""
    Dear User,

    We received a request to log in to your account. For security purposes, we have provided a secure, passwordless login link. Please click the link below to access your account:

    {login_link}

    This link is valid for 5 minutes. If you did not request this login, please ignore this email or contact our support team immediately.

    Thank you for choosing our services.

    Best regards,  
    Support Team  
    """
    msg = Message(subject, recipients=[email], body=body)
    mail.send(msg)
