import re
import bcrypt
from email_validator import validate_email, EmailNotValidError


def hash_password(password: str) -> bytes:
    '''Hashes password.'''
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


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
        if not any(char.isdigit() for char in self.data['passwd']):
            return False
        if not any(char.isalpha() for char in self.data['passwd']):
            return False
        if not any(char.isupper() for char in self.data['passwd']):
            return False
        return True

    def validate_username(self) -> bool:
        '''Checks if username is valid.'''
        if len(self.data['username']) < 4:
            return False
        if not re.match('^[a-zA-Z0-9]+$', self.data['username']):
            return False
        return True
