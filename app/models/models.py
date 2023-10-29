import re
from sqlalchemy import Boolean, Column, ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
from .base_model import BaseModel, Base


class Role(Base, BaseModel):
    '''Model for roles.'''
    __tablename__ = 'roles'

    role = Column(String(255), nullable=False, unique=True)
    users = relationship('User', backref='role', lazy=True)

    def __init__(self, role: str) -> None:
        '''Initialize role.'''
        self.role = role

    def __str__(self) -> str:
        '''String representation of role.'''
        return f'<Role {self.id} {self.role}>'

    def __repr__(self) -> str:
        '''String representation of role.'''
        return f'Role("{self.role}")'


class User(Base, BaseModel):
    '''Model for users.'''
    __tablename__ = 'users'

    email_address = Column(String(255), nullable=False, unique=True)
    username = Column(String(255), nullable=False, unique=True)
    passwd = Column(String(255), nullable=False)
    role_id = Column(String(255), ForeignKey('roles.id'), nullable=False)
    profile = relationship('Profile', backref='user', lazy=True)
    is_verified = Column(Boolean, nullable=False, default=False)

    def __init__(self, email_address: str, username: str,
                 passwd: str, role_id: str) -> None:
        '''Initialize user.'''
        self.email_address = email_address
        self.username = username
        self.passwd = passwd
        self.role_id = role_id

    @hybrid_property
    def email(self) -> str:
        '''Getter for email.'''
        return self._email

    @email.setter
    def email(self, email: str) -> None:
        '''Setter for email.'''
        if len(email) < 1:
            raise Exception('Email cannot be empty.')
        pattern = r'^[a-zA-Z][a-zA-Z0-9.-_]*@[a-zA-Z0-9]+.[a-zA-Z]+'
        result = re.search(pattern, email)

        # check if result is None
        if result is None:
            raise Exception('Invalid email address.')
        self._email = result.string

    @hybrid_property
    def passwd(self) -> str:
        '''Getter for password.'''
        return self._passwd

    @passwd.setter
    def passwd(self, passwd: str) -> None:
        '''Setter for password.'''
        if len(passwd) < 8:
            raise Exception('Password must be 8 or more characters.')
        self._passwd = passwd

    def __str__(self) -> str:
        '''String representation of user.'''
        return f'<User {self.id} {self.username}>'

    def __repr__(self) -> str:
        '''String representation of user.'''
        return f'User("{self.email_address}", "{self.username}", "{self.passwd}", "{self.role_id}")'


class Profile(Base, BaseModel):
    '''Model for user profiles.'''
    __tablename__ = 'profiles'

    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    gender = Column(String(255), nullable=False)
    nationality = Column(String(255), nullable=False)
    telephone = Column(String(255), nullable=False)
    user_id = Column(String(255), ForeignKey('users.id'), nullable=False, unique=True)

    def __init__(self, first_name, last_name, gender, nationality, telephone, user_id):
        '''Initialize profile.'''
        self.first_name = first_name
        self.last_name = last_name
        self.gender = gender
        self.nationality = nationality
        self.telephone = telephone
        self.user_id = user_id

    def __str__(self):
        '''String representation of profile.'''
        return f'<Profile {self.id} {self.first_name} {self.last_name}>'

    def __repr__(self):
        '''String representation of profile.'''
        return f'Profile("{self.first_name}", "{self.last_name}", "{self.gender}", "{self.nationality}", "{self.telephone}", "{self.user_id}")'


class Quote(Base, BaseModel):
    '''Model for quotes.'''
    __tablename__ = 'quotes'

    quote = Column(String(255), nullable=False, unique=True)
    author = Column(String(255), nullable=False)
    user_id = Column(String(255), ForeignKey('users.id'), nullable=False)
    user = relationship('User', backref='quotes', lazy=True)

    def __init__(self, quote, author, user_id):
        '''Initialize quote.'''
        self.quote = quote
        self.author = author
        self.user_id = user_id

    def __str__(self):
        '''String representation of quote.'''
        return f'<Quote {self.id} {self.quote}>'

    def __repr__(self):
        '''String representation of quote.'''
        return f'Quote("{self.author}", "{self.quote}", {self.user_id})'
