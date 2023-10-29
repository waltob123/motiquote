import os
from dotenv import load_dotenv
from flask import (abort, Blueprint, render_template, request,
                   redirect, url_for, flash)
from sqlalchemy.exc import IntegrityError
from .utils import hash_password, ValidateCredentials
from .verify import create_token, send_verification_email
from app.models.models import User, Role
from app.database.db import session

load_dotenv()

auth = Blueprint('auth', __name__, url_prefix='/auth')


@auth.errorhandler(404)
def page_not_found(e):
    '''404 page.'''
    return render_template('errors/404.html'), 404


# Authentication for normal users
@auth.route('/register', methods=['GET'], strict_slashes=True)
def register():
    '''Register page.'''
    return render_template('auth/register.html')


@auth.route('/register', methods=['POST'], strict_slashes=True)
def create_user():
    '''Create user.'''
    request_data = request.form.to_dict()
    
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

    s = session()
    request_data['passwd'] = hash_password(request_data['passwd'])  # set password to hashed password
    
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
    send_verification_email(user.email_address, sender=os.environ.get('MAIL_USERNAME'),
                            verification_link=f"{os.environ.get('DOMAIN')}/{url_for('verify.verify_email')}?token={token}")
    flash('Account created successfully. Please check your email for verification link.')
    return redirect(url_for('auth.login'))


@auth.route('/login', methods=['GET'], strict_slashes=True)
def login():
    '''Login page.'''
    return render_template('auth/login.html')


@auth.route('/login', methods=['POST'], strict_slashes=True)
def authenticate_user():
    '''Authenticate user.'''
    return 'User authenticated'


# Authentication for admin users
@auth.route('/admin/register', methods=['GET'], strict_slashes=True)
def admin_register():
    '''Admin register page.'''
    return render_template('auth/admin_register.html')


@auth.route('/admin/register', methods=['POST'], strict_slashes=True)
def create_admin_user():
    '''Create admin user.'''
    request_data = request.form.to_dict()
    validation = ValidateCredentials(request_data)
    if not validation.validate_email():
        flash(validation.errors.get('email'))
        return redirect(url_for('auth.admin_register'))
    if not validation.validate_password():
        flash(validation.errors.get('password'))
        return redirect(url_for('auth.admin_register'))
    if not validation.validate_username():
        flash(validation.errors.get('username'))
        return redirect(url_for('auth.admin_register'))

    return 'Admin user created'

@auth.route('/admin/login', methods=['GET'], strict_slashes=True)
def admin_login():
    '''Admin login page.'''
    return render_template('auth/admin_login.html')


@auth.route('/admin/login', methods=['POST'], strict_slashes=True)
def authenticate_admin_user():
    '''Authenticate admin user.'''
    return 'Admin user authenticated'
