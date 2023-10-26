from flask import Blueprint, render_template

users = Blueprint('users', __name__)


@users.route('/register', methods=['GET'], strict_slashes=True)
def register():
    return 'Register'
