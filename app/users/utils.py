import bcrypt


def hash_password(password):
    '''Hashes password.'''
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
