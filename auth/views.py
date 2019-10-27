# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging
import time

from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import models
from django.http import JsonResponse
from hashlib import sha256
from Crypto.Cipher import AES

from common.models import UserTab
from common import common_response, constant
from common.auth import log_request, AESCipher
from common.common_lib import random_session, random_salt, random_verify_code
from common.validator import validate_schema
from common.validator import validate_username, validate_password_hash, validate_salt

from common.modelmanager import UserManager

log = logging.getLogger('entry_task')


@log_request
def signup(request):

    return JsonResponse({
        'status': common_response.SUCCESS_STATUS,
        'payload': {
            'salt': random_salt()
        }
    })


complete_signup_form = {
    'type': 'object',
    'properties': {
        'username': {
            'type': 'string',
            'minLength': constant.MIN_USERNAME_LENGTH,
            'maxLength': constant.MAX_USERNAME_LENGTH
        },
        'email': {
            'type': 'string',
            'format': 'email',
        },
        'password_hash': {
            'type': 'string',
            'minLength': constant.PASSWORD_HASH_LENGTH,
            'maxLength': constant.PASSWORD_HASH_LENGTH
        },
        'salt': {
            'type': 'string',
            'minLength': constant.SALT_LENGTH,
            'maxLength': constant.SALT_LENGTH
        }
    },
    'required': ['username', 'email', 'password_hash', 'salt']
}


@log_request
@validate_schema(schema=complete_signup_form)
def complete_signup(request, form_data):
    username = form_data['username']
    password_hash = form_data['password_hash']
    salt = form_data['salt']
    email = form_data['email']

    if not validate_username(username):
        return JsonResponse(common_response.INVALID_USERNAME_RESPONSE)

    try:
        validate_email(email)
    except ValidationError:
        return JsonResponse(common_response.INVALID_EMAIL_RESPONSE)

    if not validate_password_hash(password_hash):
        return JsonResponse(common_response.INVALID_REQUEST_RESPONSE)

    if not validate_salt(salt):
        return JsonResponse(common_response.INVALID_REQUEST_RESPONSE)

    if UserTab.objects.filter(username=username).exists():
        return JsonResponse(common_response.USERNAME_EXISTS_RESPONSE)

    if UserTab.objects.filter(email=email).exists():
        return JsonResponse(common_response.EMAIL_USED_RESPONSE)

    new_user = UserManager.create_user(
        username=username,
        email=email,
        salt=salt,
        password_hash=password_hash
    )

    if new_user:
        return JsonResponse({
            'status': common_response.SUCCESS_STATUS,
            'payload': {
                'user': {
                    'id': new_user.id,
                    'username': new_user.username,
                    'email': new_user.email,
                    'created_at': new_user.created_at,
                }
            }
        })
    else:
        return JsonResponse(common_response.INVALID_REQUEST_RESPONSE)


login_form = {
    'type': 'object',
    'properties': {
        'username': {
            'type': 'string',
            'minLength': constant.MIN_USERNAME_LENGTH,
            'maxLength': constant.MAX_USERNAME_LENGTH
        },
    },
    'required': ['username']
}


@log_request
@validate_schema(login_form)
def login(request, form_data):
    username = form_data['username']

    user = UserManager.get_user_by_username(username=username)

    if not user:
        return JsonResponse(common_response.USERNAME_NOT_FOUND_RESPONSE)

    verify_code = random_verify_code()

    cache.set(
        'code.' + user.username,
        verify_code,
        constant.SESSION_TIMEOUT
    )

    return JsonResponse({
        'status': common_response.SUCCESS_STATUS,
        'payload': {
            'salt': user.salt,
            'verify_code': verify_code
        }
    })


complete_login_form = {
    'type': 'object',
    'properties': {
        'username': {
            'type': 'string',
            'minLength': constant.MIN_USERNAME_LENGTH,
            'maxLength': constant.MAX_USERNAME_LENGTH
        },
        'encrypted_password': {
            'type': 'string',
            'minLength': constant.PASSWORD_HASH_LENGTH,
            'maxLength': constant.PASSWORD_HASH_LENGTH
        },
    },
    'required': ['username', 'password_hash']
}


@log_request
@validate_schema(schema=complete_login_form)
def complete_login(request, form_data):
    username = form_data['username']
    encrypted_password = form_data['encrypted_password']

    verify_code = cache.get('code.' + username)

    if not verify_code:
        return JsonResponse(common_response.INVALID_REQUEST_RESPONSE)

    try:
        user = UserTab.objects.get(username=username)
    except models.ObjectDoesNotExist:
        return JsonResponse(common_response.USERNAME_NOT_FOUND_RESPONSE)

    cipher = AESCipher(key=sha256(user.password_hash + verify_code).hexdigest())
    password_hash = cipher.decrypt(encrypted_password)

    # cipher = AES.new(sha256(user.password_hash + verify_code).hexdigest())
    # password_hash = cipher.decrypt(encrypted_password)

    if user.password_hash != password_hash:
        return JsonResponse(common_response.WRONG_PASSWORD_RESPONSE)

    session_id = random_session()
    cache.set(
        session_id,
        {
            'id': user.id,
            'username': user.username
        },
        constant.SESSION_TIMEOUT
    )

    res = JsonResponse({
        'status': common_response.SUCCESS_STATUS,
        'payload': {
            'session_id': session_id
        }
    })

    res.set_cookie('session_id', session_id, httponly=True)

    return res

