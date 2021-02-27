import datetime
import jwt
from flask import current_app

illegal_characters = ['!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~']


def check_spell(username, password):
    """check_spell.

    :param username:
    :param password:
    """
    for c in username:
        if c in illegal_characters:
            return False

    for c in password:
        if c in illegal_characters:
            return False

    return True

def check_spell(auth_string):
    for c in auth_string:
        if c in illegal_characters:
            return False

    return True

def escape(string):
    #TODO: adding safe 
    return string

def token_retrieve(token):
    return jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])

def token_gen(user_id):
    payload = {
            "exp": datetime.datetime.now() + datetime.timedelta(days=7),
            "iat": datetime.datetime.now(),
            "sub": user_id
            }
    token = jwt.encode(
        payload,
        current_app.config['SECRET_KEY'],
        algorithm='HS256'
        )

    return token
