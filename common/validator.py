# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import logging
import string
from functools import wraps

import jsonschema
from django.http import JsonResponse

log = logging.getLogger('entry_task')

from common import common_response, constant


def validate_username(username):
    return isinstance(username, basestring) \
           and constant.MIN_USERNAME_LENGTH < len(username) < constant.MAX_USERNAME_LENGTH and username.isalnum()


def validate_salt(salt):
    return isinstance(salt, basestring) and len(salt) == constant.SALT_LENGTH and salt.isalnum()


def validate_verify_code(verify_code):
    return isinstance(verify_code, basestring) and len(verify_code) == constant.SALT_LENGTH and verify_code.isalnum()


def validate_password_hash(password_hash):
    return isinstance(password_hash, basestring) and len(password_hash) == constant.PASSWORD_HASH_LENGTH \
           and all(x in string.hexdigits for x in password_hash)


def validate_schema(schema):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            request = args[0]
            try:
                form_data = json.loads(request.POST.get('form_data'))
                jsonschema.validate(instance=form_data, schema=schema)
            except (jsonschema.ValidationError, TypeError, ValueError) as e:
                log.info(e)
                return JsonResponse(common_response.INVALID_REQUEST_RESPONSE)

            return f(*args, form_data=form_data, **kwargs)

        return wrapper

    return decorator

