# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging
import time

from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import models
from django.http import JsonResponse

import constant
from api.models import User
from common import common_response
from common.auth import log_request
from common.common_lib import random_session, random_salt
from common.validator import validate_schema
from common.validator import validate_username, validate_password_hash, validate_salt

log = logging.getLogger('entry_task')


signup_form = {
    'type': 'object',
    'properties': {
        'username': {
            'type': 'string',
            'minLength': constant.MIN_USERNAME_LENGTH,
            'maxLength': constant.MAX_USERNAME_LENGTH
        },
        'email': {
            'type': 'string',
            'format': 'email'
        }
    },
    'required': ['username', 'email']
}


@log_request
@validate_schema(schema=signup_form)
def signup(request):
    username = request.POST['username']
    email = request.POST['email']

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
def complete_signup(request):
    username = request.POST['username']
    password_hash = request.POST['password_hash']
    salt = request.POST['salt']
    email = request.POST['email']

    if User.objects.filter(username=username).exists():
        return JsonResponse(common_response.USERNAME_EXISTS_RESPONSE)

    if User.objects.filter(email=email).exists():
        return JsonResponse(common_response.EMAIL_USED_RESPONSE)

    # TODO use password_hash from user instead
    # password_hash = hashlib.md5(username + salt).hexdigest()

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

    cur_time = time.time()

    new_user = User.objects.create(
        username=username,
        password_hash=password_hash,
        email=email,
        salt=salt,
        created_at=cur_time,
        modified_at=cur_time
    )

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
def login(request):
    username = request.POST['username']

    try:
        user = User.objects.get(username=username)
    except models.ObjectDoesNotExist:
        return JsonResponse(common_response.USERNAME_NOT_FOUND_RESPONSE)

    return JsonResponse({
        'status': common_response.SUCCESS_STATUS,
        'payload': {
            'salt': user.salt
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
        'password_hash': {
            'type': 'string',
            'minLength': constant.PASSWORD_HASH_LENGTH,
            'maxLength': constant.PASSWORD_HASH_LENGTH
        },
    },
    'required': ['username', 'password_hash']
}


@log_request
@validate_schema(schema=complete_login_form)
def complete_login(request):
    username = request.POST['username']
    password_hash = request.POST['password_hash']

    try:
        user = User.objects.get(username=username)
    except models.ObjectDoesNotExist:
        return JsonResponse(common_response.USERNAME_NOT_FOUND_RESPONSE)

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

