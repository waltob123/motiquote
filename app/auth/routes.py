import os
from dotenv import load_dotenv
from flask import (abort, Blueprint, render_template, request,
                   redirect, url_for, flash)
from flask_login import current_user, login_required, login_user, logout_user
from app import app, login_manager
from sqlalchemy.exc import IntegrityError
from .utils import check_password, hash_password, send_password_reset_email
from .verify import create_token, send_verification_email, verify_token
from .forms import ForgotPasswordForm, LoginForm, RegisterForm, ResetPasswordForm
from app.models.models import User, Role
from app.database.db import session

load_dotenv()

auth = Blueprint('auth', __name__, url_prefix='/auth')


@login_manager.user_loader
def load_user(user_id):
    '''Load user.'''
    s = session()
    user = s.query(User).filter_by(id=user_id).first()
    s.close()
    return user


# Register new user ########
############################
############################
@auth.route('/register', methods=['GET'], strict_slashes=True)
def register():
    '''Register page.'''
    # redirect if user is already logged in
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    # create form
    form = RegisterForm()
    return render_template('auth/register.html', form=form)


@auth.route('/register', methods=['POST'], strict_slashes=True)
def create_user():
    '''Create user.'''
    request_data = request.form.to_dict()  # get form data
    form_data = RegisterForm(**request_data)  # get form data

    if not form_data.validate_on_submit():
        if form_data.errors.get('email_address'):
            flash(message=form_data.errors.get('email_address')[0], category='error')
        if form_data.errors.get('username'):
            flash(message=form_data.errors.get('username')[0], category='error')
        if form_data.errors.get('password'):
            flash(message=form_data.errors.get('password')[0], category='error')
        if form_data.errors.get('confirm_password'):
            flash(message=form_data.errors.get('confirm_password')[0], category='error')
        return redirect(url_for('auth.register'))

    s = session()  # create session
    request_data['password'] = hash_password(request_data['password'])  # set password to hashed password
    
    try:
        role = s.query(Role).filter_by(role='user').first()
        request_data['role_id'] = role.id  # set role to user
    except (AttributeError, KeyError):
        s.close()
        abort(500, description='Role does not exist') # abort if role does not exist

    user = User(email_address=request_data['email_address'], username=request_data['username'],
                password=request_data['password'], role_id=request_data['role_id'])
    s.add(user)
    try:
        s.commit()
    except IntegrityError as e:
        s.close()
        flash(message='User already exists', category='error')
        return redirect(url_for('auth.register'))
    token = create_token(user)
    send_verification_email(user.email_address, sender=app.config['MAIL_USERNAME'],
                           token=token)
    flash(message='Account created successfully. Please check your email for verification link.', category='success')
    return redirect(url_for('auth.login'))


# Login user ###############
############################
############################
@auth.route('/login', methods=['GET'], strict_slashes=True)
def login():
    '''Login page.'''
    # redirect if user is already logged in
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    # create form
    form = LoginForm()
    return render_template('auth/login.html', form=form)


@auth.route('/login', methods=['POST'], strict_slashes=True)
def authenticate_user():
    '''Authenticate user.'''
    request_data = request.form.to_dict()  # get form data
    s = session()  # create session

    user = s.query(User).filter_by(email_address=request_data['email_address']).first()  # get user
    s.close()

    # check if user exists and if password matches
    if not user:
        flash(message='Account does not exist!', category='error')
        return redirect(url_for('auth.login'))

    password_match = check_password(str(request_data['password']), user.password)

    if not password_match:
        flash(message='Password provided is incorrect!', category='error')
        return redirect(url_for('auth.login'))

    if not user.is_verified:
        flash(message='Account is not verified. Please check your email for verification link.', category='info')
        return redirect(url_for('auth.login'))

    # login user
    login_user(user)
    flash(message='You have been logged in successfully.', category='success')

    return redirect(url_for('quotes.get_quotes'))


@auth.route('/logout', methods=['GET'], strict_slashes=True)
@login_required
def logout():
    '''Logout user.'''
    logout_user()
    flash(message='You have been logged out successfully.', category='info')
    return redirect(url_for('auth.login'))


# Forgot password #########
###########################
###########################
@auth.route('/forgot-password', methods=['GET'], strict_slashes=True)
def forgot_password():
    '''Forgot password page.'''
    form = ForgotPasswordForm()
    return render_template('auth/forgot-password.html', form=form)


@auth.route('/forgot-password', methods=['POST'], strict_slashes=True)
def send_reset_link():
    '''Send reset password email.'''
    request_data = request.form.to_dict()
    form = ForgotPasswordForm(**request_data)

    s = session()
    user = s.query(User).filter_by(email_address=form.data.get('email_address')).first()

    if not user:
        s.close()
        flash(message='User not found!', category='error')
        return redirect(url_for('auth.forgot_password'))

    token = create_token(user)
    username = user.profile[0].first_name + ' ' + user.profile[0].last_name
    send_password_reset_email(email=user.email_address, sender=app.config['MAIL_USERNAME'], template='mail/reset-password.html', token=token, username=username)

    flash(message='Reset password link sent!', category='success')
    return redirect(url_for('auth.login'))


# Reset password ##########
###########################
###########################
@auth.route('/reset-password', methods=['GET'], strict_slashes=True)
def reset_password():
    '''Reset password page.'''
    form = ResetPasswordForm()
    token = request.args.get('token')
    payload = verify_token(token)

    if payload == 'Token is invalid!' or payload == 'No token provided!':
        flash(message=payload, category='error')
        return render_template('auth/verification.html')

    if payload == 'Token has expired!':
        flash(message=payload, category='error')
        return render_template('auth/verification.html', token=token, reset=True)
    return render_template('auth/reset-password.html', form=form, token=token)


@auth.route('/reset-password', methods=['POST'], strict_slashes=True)
def change_password():
    '''Reset password.'''
    request_data = request.form.to_dict()
    form_data = ResetPasswordForm(**request_data)

    if not form_data.validate_on_submit():
        if form_data.errors.get('email_address'):
            flash(message=form_data.errors.get('email_address')[0], category='error')
        if form_data.errors.get('password'):
            flash(message=form_data.errors.get('password')[0], category='error')
        if form_data.errors.get('confirm_password'):
            flash(message=form_data.errors.get('confirm_password')[0], category='error')
        return redirect(url_for('auth.reset_password'))
    
    s = session()
    user = s.query(User).filter_by(email_address=request_data['email_address']).first()
    if not user:
        s.close()
        flash(message='User not found!', category='error')
        return redirect(url_for('auth.reset_password'))
    user.password = hash_password(form_data.password.data)
    s.commit()
    flash(message='Password reset successfully!', category='success')
    return redirect(url_for('auth.login'))
