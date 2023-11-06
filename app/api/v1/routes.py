from flask import abort, Blueprint, jsonify, request, url_for
from app import app
from app.models.models import Quote
from app.database.db import session

api = Blueprint('api', __name__, url_prefix='/api/v1')


@api.route('quotes/<string:quote_id>', methods=['GET'], strict_slashes=True)
def get_quote(quote_id):
    '''
    Retrieve a quote by its ID.

    Args:
        quote_id (int): The ID of the quote to retrieve.

    Returns:
        A JSON representation of the quote.

    Raises:
        404 error if the quote is not found.
    '''
    s = session()
    quote = s.query(Quote).filter_by(id=quote_id, approved=True).first()
    if not quote:
        abort(404, f'Quote with ID {quote_id} not found')
    
    result = {
        'quote': quote.quote,
        'category': quote.category.category,
        'author': quote.author,
        'created_at': quote.created_at,
        'quote_url': url_for('api.get_quote', quote_id=quote.id, _external=True)
    }
    
    return jsonify(result), 200


@api.route('quotes', methods=['GET'], strict_slashes=True)
def get_quotes():
    '''
    Retrieve all quotes.

    Returns:
        A JSON representation of all quotes.
    '''
    s = session()
    quotes = s.query(Quote).filter_by(approved=True).all()
    result = []
    for quote in quotes:
        result.append({
            'quote': quote.quote,
            'category': quote.category.category,
            'author': quote.author,
            'created_at': quote.created_at,
            'quote_url': url_for('api.get_quote', quote_id=quote.id, _external=True)
        })
    return jsonify(result), 200


@api.route('quotes/search', methods=['GET'], strict_slashes=True)
def search_quotes():
    '''
    Search quotes by author.

    Returns:
        A JSON representation of all quotes matching the search term.
    '''

    request_args = request.args.to_dict()  # get request args as a dict

    # check if search term is present
    if 'author' not in request_args:
        abort(400, 'Missing search term')

    s = session()  # create a session

    # search for quotes by author
    quotes = s.query(Quote).filter_by(author=request_args.get('author')).filter_by(approved=True).all()

    # convert quotes to a list of dicts
    results = [{
        'quote': quote.quote,
        'category': quote.category.category,
        'author': quote.author,
        'created_at': quote.created_at,
        'quote_url': url_for('api.get_quote', quote_id=quote.id, _external=True)} for quote in quotes]

    return jsonify(results), 200
