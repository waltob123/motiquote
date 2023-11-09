from flask_login import UserMixin
from sqlalchemy import Boolean, Column, ForeignKey, String
from sqlalchemy.orm import relationship
from .base_model import BaseModel, Base


class Category(Base, BaseModel):
    '''Model for categories.'''
    __tablename__ = 'categories'

    category = Column(String(255), nullable=False, unique=True, default='General')

    def __init__(self, category):
        '''Initialize category.'''
        self.category = category

    def __str__(self):
        return f'<Category {self.id} {self.category}>'

    def __repr__(self):
        return f'Category("{self.category}")'


class Country(Base, BaseModel):
    '''Model for countries'''
    __tablename__ = 'countries'

    country = Column(String(255), nullable=False, unique=True)
    code = Column(String(255), nullable=False, unique=True)

    def __init__(self, country, code):
        '''Initialize country'''
        self.country = country
        self.code = code

    def __str__(self):
        return f'<Country {self.id} {self.country}>'

    def __repr__(self):
        return f'Country("{self.country}")'


class Gender(Base, BaseModel):
    '''Model for genders'''
    __tablename__ = 'genders'

    gender = Column(String(255), nullable=False, unique=True)

    def __init__(self, gender):
        '''Initialize gender'''
        self.gender = gender

    def __str__(self):
        return f'<Gender {self.id} {self.gender}>'

    def __repr__(self):
        return f'Gender("{self.gender}")'


class Profile(Base, BaseModel):
    '''Model for user profiles.'''
    __tablename__ = 'profiles'

    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    telephone = Column(String(255), nullable=False)
    gender_id = Column(String(255), ForeignKey('genders.id'), nullable=False)
    country_id = Column(String(255), ForeignKey('countries.id'), nullable=False,)
    user_id = Column(String(255), ForeignKey('users.id'), nullable=False, unique=True)
    gender = relationship('Gender', backref='profiles', lazy=True)
    country = relationship('Country', backref='profiles', lazy=True)

    def __init__(self, country_id, first_name, last_name, gender_id, telephone, user_id):
        '''Initialize profile.'''
        self.country_id = country_id
        self.first_name = first_name
        self.last_name = last_name
        self.gender_id = gender_id
        self.telephone = telephone
        self.user_id = user_id

    def __str__(self):
        '''String representation of profile.'''
        return f'<Profile {self.id} {self.first_name} {self.last_name}>'

    def __repr__(self):
        '''String representation of profile.'''
        return f'Profile("{self.first_name}", "{self.last_name}", "{self.gender_id}", "{self.country_id}", "{self.telephone}", "{self.user_id}")'


class Quote(Base, BaseModel):
    '''Model for quotes.'''
    __tablename__ = 'quotes'

    quote = Column(String(255), nullable=False, unique=True)
    author = Column(String(255), nullable=False)
    approved = Column(Boolean, nullable=False, default=False)
    user_id = Column(String(255), ForeignKey('users.id'), nullable=False)
    category_id = Column(String(255), ForeignKey('categories.id'), nullable=False)
    user = relationship('User', backref='quotes', lazy=True)
    category = relationship('Category', backref='quotes', lazy=True)

    def __init__(self, category_id, quote, author, user_id):
        '''Initialize quote.'''
        self.quote = quote
        self.author = author
        self.user_id = user_id
        self.category_id = category_id

    def __str__(self):
        '''String representation of quote.'''
        return f'<Quote {self.id} {self.quote}>'

    def __repr__(self):
        '''String representation of quote.'''
        return f'Quote("{self.author}", "{self.quote}", {self.user_id})'


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


class User(Base, UserMixin, BaseModel):
    '''Model for users.'''
    __tablename__ = 'users'

    email_address = Column(String(255), nullable=False, unique=True)
    username = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    role_id = Column(String(255), ForeignKey('roles.id'), nullable=False)
    profile = relationship('Profile', backref='user', lazy=True)
    is_verified = Column(Boolean, nullable=False, default=False)

    def __init__(self, email_address: str, username: str,
                 password: str, role_id: str) -> None:
        '''Initialize user.'''
        self.email_address = email_address
        self.username = username
        self.password = password
        self.role_id = role_id

    def get_id(self) -> str:
        '''Get user id.'''
        return self.id

    def __str__(self) -> str:
        '''String representation of user.'''
        return f'<User {self.id} {self.username}>'

    def __repr__(self) -> str:
        '''String representation of user.'''
        return f'User("{self.email_address}", "{self.username}", "{self.password}", "{self.role_id}")'
