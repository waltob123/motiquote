import os
import jwt
from datetime import datetime, timedelta
from flask import flash, Blueprint, request, render_template, redirect, url_for
from dotenv import load_dotenv
from flask_mail import Message
from app import app, mail
from ..models.models import User
from ..database.db import session
from .utils import send_password_reset_email


load_dotenv()

verify = Blueprint('verify', __name__, url_prefix='/verify')


def create_token(user):
    '''Create token.'''
    payload = {
        'email_address': user.email_address,
        'exp': datetime.utcnow() + timedelta(days=1)
    }
    token = jwt.encode(payload, os.environ.get('SECRET_KEY'), algorithm='HS256')
    return token


def send_verification_email(email: str, sender: str, token: str):
    message = Message(
        'Account Verification',
        recipients=[email],
        sender=sender
    )

    message.html = render_template('mail/verify-account.html', domain=app.config['DOMAIN'], token=token, url=url_for('verify.verify_email'))
    mail.send(message)


def verify_token(token=None):
    '''Verify token.'''
    if token is None:
        return 'No token provided!'
    try:
        payload = jwt.decode(token, os.environ.get('SECRET_KEY'), algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return 'Token has expired!'
    except jwt.InvalidTokenError:
        return 'Token is invalid!'
    return payload


# token routes
@verify.route('/request', methods=['GET'], strict_slashes=True)
def request_token():
    '''Request token.'''
    token = request.args.get('token')
    s = session()

    payload = jwt.decode(token, os.environ.get('SECRET_KEY'), algorithms=['HS256'], options={'verify_signature': False})

    user = s.query(User).filter_by(email_address=payload.get('email_address')).first()

    if not user:
        s.close()
        flash(message='User not found!', category='error')
        return render_template('auth/verification.html')

    if user.is_verified:
        s.close()
        flash(message='Account already verified!', category='info')
        return redirect(url_for('auth.login'))

    new_token = create_token(user)
    send_verification_email(user.email_address, sender=app.config['DOMAIN'],
                            token=new_token)
    flash(message='Verification email sent!', category='success')
    return redirect(url_for('auth.login'))


@verify.route('/reset-password/request', methods=['GET'], strict_slashes=True)
def reset_request_token():
    '''Request reset password token.'''
    token = request.args.get('token')
    s = session()

    payload = jwt.decode(token, os.environ.get('SECRET_KEY'), algorithms=['HS256'], options={'verify_signature': False})

    user = s.query(User).filter_by(email_address=payload.get('email_address')).first()

    if not user:
        s.close()
        flash(message='User not found!', category='error')
        return render_template('auth/verification.html')
    new_token = create_token(user)
    send_password_reset_email(email=user.email_address, sender=os.environ.get('MAIL_USERNAME'), template='mail/reset-password.html', token=new_token)
    

@verify.route('', methods=['GET'])
def verify_email():
    '''Verify email address.'''
    token = request.args.get('token')
    s = session()
    payload = verify_token(token)
    if payload == 'Token is invalid!' or payload == 'No token provided!':
        flash(message=payload, category='error')
        return render_template('auth/verification.html')

    if payload == 'Token has expired!':
        flash(message=payload, category='error')
        return render_template('auth/verification.html', token=token)

    user = s.query(User).filter_by(email_address=payload.get('email_address')).first()

    if not user:
        s.close()
        flash(message='User not found! Check if verification is correct.', category='error')
        return render_template('auth/verification.html', domain=False)
    user.is_verified = True
    s.commit()
    s.close()
    flash(message='Account verified successfully!', category='success')
    return redirect(url_for('auth.login'))
