# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import random
import string

from django.core.cache import cache


def get_user(request):
    if 'session_id' not in request.COOKIES:
        return None
    user_id = cache.get(request.COOKIES.get('session_id'))

    return user_id


def validate_username(username):
    return isinstance(username, basestring) and 4 < len(username) < 33 and username.isalnum()


def validate_salt(salt):
    return isinstance(salt, basestring) and len(salt) == 8 and salt.isalnum()


def validate_password_hash(password_hash):
    return isinstance(password_hash, basestring) and len(password_hash) == 32 and all(x in string.hexdigits for x in password_hash)


ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def random_alnum(length):
    s = []
    for i in range(length):
        s.append(random.choice(ALPHABET))

    return "".join(s)


def random_salt():
    return random_alnum(8)


def random_session():
    return random_alnum(16)
