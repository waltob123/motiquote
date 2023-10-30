import os
import jwt
from datetime import datetime, timedelta
from flask import flash, Blueprint, request, render_template, redirect, url_for
from dotenv import load_dotenv
from flask_mail import Message
from app import app, mail
from ..models.models import User
from ..database.db import session


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


def verify_token(token=None):
    '''Verify token.'''
    if token is None:
        return 'No token provided!'
    try:
        payload = jwt.decode(token, os.environ.get('SECRET_KEY'), algorithms=['HS256'])
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return 'Token is invalid!'
    return payload


def send_verification_email(email: str, sender: str, verification_link):
    message = Message(
        'Account Verification',
        recipients=[email],
        sender=sender
    )

    message.body = f'Verify your account using this link {verification_link}'
    mail.send(message)



@verify.route('/request', methods=['GET'])
def request_token():
    '''Request token.'''
    token = request.args.get('token')
    s = session()

    payload = verify_token(token)

    if payload == 'Token is invalid!' or payload == 'No token provided!':
        flash(message=payload, category='error')
        return render_template('auth/verification.html', token=token, domain=os.environ.get('DOMAIN'))

    user = s.query(User).filter_by(email_address=payload.get('email_address')).first()

    if not user:
        s.close()
        flash(message='User not found! Check if verification is correct.', category='error')
        return render_template('auth/verification.html', domain=False)
    new_token = create_token(user)
    send_verification_email(user.email_address, sender=os.environ.get('MAIL_USERNAME'),
                            verification_link=f"{app.config['DOMAIN']}{url_for('verify.verify_email')}?token={new_token}")
    flash(message='Verification email sent!', category='success')
    return redirect(url_for('auth.login'))


@verify.route('', methods=['GET'])
def verify_email():
    '''Verify email address.'''
    token = request.args.get('token')
    s = session()
    payload = verify_token(token)
    if payload == 'Token is invalid!' or payload == 'No token provided!':
        flash(message=payload, category='error')
        return render_template('auth/verification.html', token=token, domain=os.environ.get('DOMAIN'))

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
