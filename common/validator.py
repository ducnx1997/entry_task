# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from functools import wraps
import jsonschema
import string
from django.http import JsonResponse
import constant

from common import common_response


def validate_username(username):
    return isinstance(username, basestring) \
           and constant.MIN_USERNAME_LENGTH < len(username) < constant.MAX_USERNAME_LENGTH and username.isalnum()


def validate_salt(salt):
    return isinstance(salt, basestring) and len(salt) == constant.SALT_LENGTH and salt.isalnum()


def validate_password_hash(password_hash):
    return isinstance(password_hash, basestring) and len(password_hash) == constant.PASSWORD_HASH_LENGTH \
           and all(x in string.hexdigits for x in password_hash)


def validate_schema(schema):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            request = args[0]
            try:
                jsonschema.validate(instance=request.POST, schema=schema)
            except jsonschema.ValidationError:
                return JsonResponse(common_response.INVALID_REQUEST_RESPONSE)

            return f(*args, **kwargs)

        return wrapper

    return decorator

