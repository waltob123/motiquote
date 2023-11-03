from flask import Blueprint, flash, jsonify, render_template, redirect, url_for, request
from flask_login import current_user, login_required
from sqlalchemy.exc import IntegrityError
from ..models.models import Quote, Category
from ..database.db import session
from .forms import QuoteForm
from textblob import TextBlob

quotes = Blueprint('quotes', __name__, url_prefix='/quotes')


@quotes.route('', methods=['GET'], strict_slashes=True)
@login_required
def get_quotes():
    '''
    Retrieves all quotes by the current user and renders it on the page.

    Returns:
        str: The rendered HTML template for the quote page.
    '''
    # create database session
    s = session()
    
    quote_form = QuoteForm()

    # query database for all quotes associated to current user
    quotes = [quote for quote in s.query(Quote).filter_by(user_id=current_user.id).join(Category).all() if quote.approved]
 
    # if there are not quotes for the user set quotes to False
    if not quotes:
        quotes = False

    return render_template('quotes/quotes.html', quotes=quotes, form=quote_form)


@quotes.route('/<string:id>', methods=['GET'], strict_slashes=True)
@login_required
def get_quote(id):
    '''
    Retrieves a single quote by the current user and renders it on the page.

    Args:
        id (str): The id of the quote to retrieve.

    Returns:
        str: The rendered HTML template for the quote page.
    '''
    # create database session
    s = session()

    # query database for quote by id
    quote = s.query(Quote).filter_by(id=id).first()

    # check if quote exists
    if quote:
        return jsonify({
            'id': quote.id,
            'quote': quote.quote,
            'author': quote.author,
            'category_id': quote.category.id,
            'quote_url': url_for('quotes.update_quote', id=quote.id),
        })

    flash(message='The quote does not exist!', category='error')
    return redirect(url_for('quotes.get_quotes'))


@quotes.route('/add', methods=['POST'], strict_slashes=True)
@login_required
def create_quote():
    '''
    Creates a new post
    
    Returns:
        str: The rendered HTML template for the quote page
    '''

    s = session()  # create database session    
    request_data = request.form.to_dict()  # convert request data to dictionary

    new_quote = Quote(quote=request_data['quote'],
                      author=request_data['author'],
                      category_id=request_data['category_id'],
                      user_id=current_user.id)  # create new quote object

    s.add(new_quote)  # add new quote to database

    blob = TextBlob(new_quote.quote)  # create TextBlob object for sentiment analysis

    sentiment = blob.sentiment.polarity

    # check if sentiment is positive
    if sentiment > 0:
        new_quote.approved = True

        try:
            s.commit()  # commit changes to database
            flash(message='Your quote has been added successfully', category='success')
        except IntegrityError:
            s.rollback()
            flash(message='The quote already exists!', category='error')

        s.close()  # close database session

    else:
        flash(message='Please check your quote again. It seems to be too negative.', category='error')

    return redirect(url_for('quotes.get_quotes'))


@quotes.route('/update/<string:id>', methods=['POST'], strict_slashes=True)
@login_required
def update_quote(id):
    '''
    Updates an existing quote.
    
    Args:
        id (str): The id of the quote to update.

    Returns:
        str: The rendered HTML template for the quote page.
    '''
    s = session()
    request_data = request.form.to_dict()  # convert request data to dictionary
    
    quote = s.query(Quote).filter_by(id=id)  # query database for quote by id

    # set values to update
    quote_update_values = {
        'quote': request_data['quote'],
        'author': request_data['author'],
        'category_id': request_data['category_id']
    }

    # check if quote exists
    if quote.first():
        quote.update(quote_update_values, synchronize_session=False)  # update quote

        # try to commit changes to database
        try:
            s.commit()
            flash(message='Your quote has been updated successfully', category='success')
        except IntegrityError:
            s.rollback()
            flash(message='The quote already exists!', category='error')    

        s.close()  # close database session
    else:
        flash(message='The quote does not exist!', category='error')
    return redirect(url_for('quotes.get_quotes'))


@quotes.route('/delete/<string:id>', methods=['GET'], strict_slashes=True)
@login_required
def delete_quote(id):
    '''
    Deletes an existing quote.
    
    Args:
        id (str): The id of the quote to delete.

    Returns:
        str: The rendered HTML template for the quote page.
    '''
    s = session()
    quote = s.query(Quote).filter_by(id=id)  # query database for quote by id

    # check if quote exists
    if quote.first():
        quote.delete(synchronize_session=False)  # delete quote
        s.commit()  # commit changes to database
        flash(message='Your quote has been deleted successfully', category='success')
    else:
        flash(message='The quote does not exist!', category='error')

    s.close()  # close database session
    return redirect(url_for('quotes.get_quotes'))
