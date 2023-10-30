import os
import jwt
from datetime import datetime, timedelta
from flask import flash, Blueprint, request, render_template, redirect, url_for
from dotenv import load_dotenv
from flask_mail import Message
from app import mail
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


@verify.route('/request', methods=['POST'])
def request_token(email_address: str):
    '''Request token.'''
    token = request.args.get('token')
    try:
        user = session.query(User).filter_by(email_address=email_address).first()
    except AttributeError:
        flash(message='User not found', category='error')
        return render_template('auth/verification.html')
    token = create_token(user)
    send_verification_email(user.email_address, sender=os.environ.get('MAIL_USERNAME'),
                            verification_link=f"{os.environ.get('DOMAIN')}{url_for('verify.verify_email')}?token={token}")
    flash(message='Verification email sent!', category='success')
    return redirect(url_for('auth.login'))


def send_verification_email(email: str, sender: str, verification_link):
    message = Message(
        'Account Verification',
        recipients=[email],
        sender=sender
    )

    message.body = f'Verify your account using this link {verification_link}'
    mail.send(message)


@verify.route('/account', methods=['GET'])
def verify_email():
    '''Verify email address.'''
    token = request.args.get('token')
    s = session()
    if not token:
        flash(message='No token provided!', category='error')
        s.close()
        return render_template('auth/verification.html', token=token, domain=os.environ.get('DOMAIN'))
    try:
        payload = jwt.decode(token, os.environ.get('SECRET_KEY'), algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        flash(message='Token has expired!', category='error')
        s.close()
        return render_template('auth/verification.html', token=token, domain=os.environ.get('DOMAIN'))
    except jwt.InvalidTokenError:
        flash(message='Token is invalid!', category='error')
        s.close()
        return render_template('auth/verification.html', token=token, domain=os.environ.get('DOMAIN'))

    user = session.query(User).filter_by(email_address=payload.get('email_address')).first()
    if not user:
        flash(message='Account does not exists!', category='error')
        s.close()
        return render_template('auth/verification.html', token=token, domain=os.environ.get('DOMAIN'))
    user.is_verified = True
    s.commit()
    s.close()
    flash(message='Account verified successfully!', category='success')
    return redirect(url_for('auth.login'))
