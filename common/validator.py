# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from functools import wraps
from jsonschema import validate, ValidationError
import string
from django.http import JsonResponse

from common import common_response


def validate_username(username):
    return isinstance(username, basestring) and 4 < len(username) < 33 and username.isalnum()


def validate_salt(salt):
    return isinstance(salt, basestring) and len(salt) == 8 and salt.isalnum()


def validate_password_hash(password_hash):
    return isinstance(password_hash, basestring) and len(password_hash) == 32 \
           and all(x in string.hexdigits for x in password_hash)


def validate_schema(schema):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            request = args[0]
            try:
                validate(instance=request.POST, schema=schema)
            except ValidationError:
                return JsonResponse(common_response.INVALID_REQUEST_RESPONSE)

            return f(*args, **kwargs)

        return wrapper

    return decorator
