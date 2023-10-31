import os
from dotenv import load_dotenv
from flask import (abort, Blueprint, render_template, request,
                   redirect, url_for, flash)
from flask_login import current_user, login_required, login_user, logout_user
from app import app, login_manager
from sqlalchemy.exc import IntegrityError
from .utils import check_password, hash_password, ValidateCredentials
from .verify import create_token, send_verification_email
from app.models.models import User, Role
from app.database.db import session

load_dotenv()

auth = Blueprint('auth', __name__, url_prefix='/auth')


@auth.errorhandler(404)
def page_not_found(e):
    '''404 page.'''
    return render_template('errors/404.html'), 404


@login_manager.user_loader
def load_user(user_id):
    '''Load user.'''
    s = session()
    user = s.query(User).filter_by(id=user_id).first()
    s.close()
    return user


# Authentication for normal users
@auth.route('/register', methods=['GET'], strict_slashes=True)
def register():
    '''Register page.'''
    # redirect if user is already logged in
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    return render_template('auth/register.html')


@auth.route('/register', methods=['POST'], strict_slashes=True)
def create_user():
    '''Create user.'''
    request_data = request.form.to_dict()  # get form data
    
    # validate data
    validation = ValidateCredentials(request_data)
    if not validation.validate_email():
        flash(validation.errors.get('email'))
        return redirect(url_for('auth.register'))
    if not validation.validate_password():
        flash(validation.errors.get('password'))
        return redirect(url_for('auth.register'))
    if not validation.validate_username():
        flash(validation.errors.get('username'))
        return redirect(url_for('auth.register'))

    s = session()  # create session
    request_data['password'] = hash_password(request_data['password'])  # set password to hashed password
    
    try:
        role = s.query(Role).filter_by(role='user').first()
        request_data['role_id'] = role.id  # set role to user
    except AttributeError:
        s.close()
        abort(500)

    user = User(**request_data)
    s.add(user)
    try:
        s.commit()
    except IntegrityError as e:
        s.close()
        flash('User already exists')
        return redirect(url_for('auth.register'))
    token = create_token(user)
    send_verification_email(user.email_address, sender=app.config['MAIL_USERNAME'],
                            verification_link=f"{app.config['DOMAIN']}{url_for('verify.verify_email')}?token={token}")
    flash('Account created successfully. Please check your email for verification link.')
    return redirect(url_for('auth.login'))


@auth.route('/login', methods=['GET'], strict_slashes=True)
def login():
    '''Login page.'''
    # redirect if user is already logged in
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    return render_template('auth/login.html')


@auth.route('/login', methods=['POST'], strict_slashes=True)
def authenticate_user():
    '''Authenticate user.'''
    request_data = request.form.to_dict()  # get form data
    s = session()  # create session

    user = s.query(User).filter_by(email_address=request_data['email_address']).first()  # get user
    s.close()

    # check if user exists and if password matches
    if not user:
        flash('Account does not exist!')
        return redirect(url_for('auth.login'))

    password_match = check_password(str(request_data['password']), user.password)

    if not password_match:
        flash('Password provided is incorrect!')
        return redirect(url_for('auth.login'))
    
    # login user
    login_user(user)
    
    return redirect(url_for('main.index'))


@auth.route('/logout', methods=['GET'], strict_slashes=True)
@login_required
def logout():
    '''Logout user.'''
    logout_user()
    return redirect(url_for('auth.login'))
