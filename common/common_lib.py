# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from django.core.cache import cache


def get_user(request):
    if 'session_id' not in request.COOKIES:
        return None
    user_id = cache.get(request.COOKIES.get('session_id'))

    return user_id


ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def random_alnum(length):
    return os.urandom(length / 2).decode('hex')


def random_salt():
    return random_alnum(8)


def random_verify_code():
    return random_alnum(8)


def random_session():
    return random_alnum(16)
