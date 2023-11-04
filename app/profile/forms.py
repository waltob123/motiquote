from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField
from wtforms.validators import DataRequired
from ..models.models import Country, Gender
from ..database.db import session

class ProfileForm(FlaskForm):
    '''
    A form for editing user profiles.

    Attributes:
        firstname (StringField): A field for the user's firstname.
        lastname (StringField): A field for the user' lastname.
        gender (SelectField): A field for the user's gender.
        country (SelectField): A field for user's country.
        telephone (StringField): A field for user's telephone.
        submit (SubmitField): A field for submitting the form.
    '''
    s = session()
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    gender_id = SelectField('Gender', validators=[DataRequired()], choices=[
        (g.id, g.gender) for g in s.query(Gender).order_by(Gender.gender).all() if g
    ])
    country_id = SelectField('Country', validators=[DataRequired()], choices=[
        (c.id, c.country) for c in s.query(Country).order_by(Country.country).all() if c
    ])
    telephone = StringField('Telephone', validators=[DataRequired()])
    submit = SubmitField('Submit')
