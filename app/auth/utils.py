import re
import bcrypt
from app import app
from email_validator import validate_email, EmailNotValidError
from flask_mail import Message
from app import mail
from flask import render_template, url_for


def hash_password(password: str) -> bytes:
    '''Hashes password.'''
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def check_password(password: str, hashed_password: bytes) -> bool:
    '''Checks if password matches hashed password.'''
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))


def send_password_reset_email(email: str, sender: str, template: str, username: str, token: str):
    message = Message(
        'Reset Account Password',
        recipients=[email],
        sender=sender
    )

    message.html = render_template(template, domain=app.config['DOMAIN'], username=username, url=url_for('auth.reset_password'), token=token)
    mail.send(message)


class ValidateCredentials:
    '''Validates registration data.'''

    def __init__(self, data: dict):
        self.data = data
        self.errors = {
            'email': 'Email address is not valid',
            'password': 'Password must be at least 8 characters long and contain at least one uppercase letter and one number',
            'username': 'Username must be at least 4 characters long and contain only letters, numbers',
        }

    def validate_email(self) -> bool:
        '''Validates email address.'''
        try:
            email = validate_email(self.data['email_address'])
        except EmailNotValidError:
            return False
        return True

    def validate_password(self) -> bool:
        '''Checks if password is valid.'''
        if len(self.data['password']) < 8:
            return False
        if not any(char.isdigit() for char in self.data['password']):
            return False
        if not any(char.isalpha() for char in self.data['password']):
            return False
        if not any(char.isupper() for char in self.data['password']):
            return False
        return True

    def validate_username(self) -> bool:
        '''Checks if username is valid.'''
        if len(self.data['username']) < 4:
            return False
        if not re.match('^[a-zA-Z0-9]+$', self.data['username']):
            return False
        return True
