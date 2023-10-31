from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import (DataRequired, Email, EqualTo, Length,
                                ValidationError)


class BaseForm(FlaskForm):
    '''Base form.'''
    email_address = StringField('Email Address', validators=[
                                DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    
    def validate_password(self, password: PasswordField) -> None:
        '''Validates password.'''
        if len(password.data) < 8:
            raise ValidationError('Password must be at least 8 characters long')
        if not any(char.isdigit() for char in password.data):
            raise ValidationError('Password must contain at least one number')
        if not any(char.isalpha() for char in password.data):
            raise ValidationError('Password must contain at least one letter')
        if not any(char.isupper() for char in password.data):
            raise ValidationError('Password must contain at least one uppercase letter')


class RegisterForm(BaseForm, FlaskForm):
    '''Form for registering a user.'''
    username = StringField('Username', validators=[DataRequired(), Length(
        min=4, max=255, message='Username must be at least 4 characters long')])
    confirm_password = PasswordField('Confirm Password', validators=[
                                     DataRequired(), EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Register')


class LoginForm(BaseForm, FlaskForm):
    '''Form for logging in a user.'''
    submit = SubmitField('Login')
