from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required
from ..database.db import session
from ..models.models import Profile
from .forms import ProfileForm

profiles = Blueprint('profiles', __name__, url_prefix='/profiles')


@profiles.route('<string:user_id>', methods=['GET'], strict_slashes=True)
@login_required
def get_profile(user_id):
    """
    Render the profile page for a given user ID.

    Args:
        id (str): The ID of the user whose profile is being requested.

    Returns:
        The rendered profile page template.
    """
    s = session()  # create database session
    form = ProfileForm()  # create profile form
    profile = s.query(Profile).filter_by(user_id=user_id).first()  # get user profile

    # check if profile exists, if it does, send it to the template along with the form
    if profile:
        s.commit()  # commit changes to database
        return render_template('profiles/profiles.html', profile=profile, form=form)
    else:  # if profile does not exist, send the form to the template
        s.rollback()  # rollback changes to database
        return render_template('profiles/profiles.html', form=form)


@profiles.route('', methods=['POST'], strict_slashes=True)
@login_required
def create_profile():
    '''
    This function creates a new user profile and saves it to the database.
    
    Returns:
        Profile page.
    '''
    s = session()  # create database session
    request_data = request.form.to_dict()  # get form data
    request_data['user_id'] = current_user.id  # add user ID to form data

    # create new profile
    profile = Profile(
        first_name=request_data['first_name'],
        last_name=request_data['last_name'],
        gender_id=request_data['gender_id'],
        country_id=request_data['country_id'],
        telephone=request_data['telephone'],
        user_id=request_data['user_id']
    )

    s.add(profile)  # add profile to database

    # commit changes to database
    try:
        s.commit()
        flash(message='Profile created successfully!', category='success')
    except Exception as e:
        s.rollback()
        flash(message='User profile exists already!', category='danger')

    s.close()  # close database session
    return redirect(url_for('profiles.get_profile', user_id=current_user.id))


@profiles.route('update/<string:user_id>/<string:profile_id>', methods=['POST'], strict_slashes=True)
@login_required
def update_profile(user_id, profile_id):
    '''
    This function updates a user profile and saves it to the database.
    
    Returns:
        Profile page.
    '''
    s = session()  # create database session
    request_data = request.form.to_dict()  # get form data

    # update profile
    profile = s.query(Profile).filter_by(id=profile_id, user_id=user_id)

    # check if profile exists, if it does, update it
    if profile.first():
        profile_values_to_update = {
            'first_name': request_data['first_name'],
            'last_name': request_data['last_name'],
            'gender_id': request_data['gender_id'],
            'country_id': request_data['country_id'],
            'telephone': request_data['telephone'],
        }
        profile.update(profile_values_to_update, synchronize_session=False)  # update profile
        
        try:
            s.commit()  # commit changes to database
            flash(message='Profile updated successfully!', category='success')
        except Exception as e:
            s.rollback()
            flash(message='User profile exists already!', category='danger')
    else:
        flash(message='Profile does not exist!', category='danger')
    return redirect(url_for('profiles.get_profile', user_id=current_user.id))
