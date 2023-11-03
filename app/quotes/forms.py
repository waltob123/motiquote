from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField
from wtforms.validators import DataRequired
from ..models.models import Category
from ..database.db import session


class QuoteForm(FlaskForm):
    """
    A form for creating a new quote.

    Attributes:
        quote (StringField): The quote text.
        author (StringField): The author of the quote.
        category (StringField): The category of the quote.
        submit (SubmitField): The submit button.
    """
    # create database session
    s = session()
    id = StringField('Id')
    quote = StringField('Quote', validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired()])
    category_id = SelectField('Category', validators=[DataRequired()], choices=[(cat.id, cat.category) for cat in s.query(Category).all()])
    submit = SubmitField('Post Quote')
