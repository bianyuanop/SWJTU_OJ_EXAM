
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

