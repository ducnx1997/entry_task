# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging
import time

from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import models
from django.http import JsonResponse
from django.utils.datastructures import MultiValueDictKeyError

import constant
from api.models import User
from common import common_response
from common.auth import log_request
from common.common_lib import random_session, random_salt
from common.validator import validate_username, validate_password_hash, validate_salt

from common.validator import validate_schema

log = logging.getLogger('entry_task')


signup_form = {
    'type': 'object',
    'properties': {
        'username': {
            'type': 'string',
            'minLength': 4,
            'maxLength': 32
        },
        'email': {
            'type': 'string',
            'format': 'email'
        }
    }
}


@validate_schema(schema=signup_form)
@log_request
def signup(request):
    try:
        username = str(request.POST['username'])
        email = str(request.POST['email'])
    except (MultiValueDictKeyError, ValueError):
        return JsonResponse(common_response.INVALID_REQUEST_RESPONSE)


    if not validate_username(username):
        return JsonResponse(common_response.INVALID_REQUEST_RESPONSE)

    if User.objects.filter(username=username).exists():
        return JsonResponse(common_response.USERNAME_EXISTS_RESPONSE)

    if User.objects.filter(email=email).exists():
        return JsonResponse(common_response.EMAIL_USED_RESPONSE)

    return JsonResponse({
        'status': 'SUCCESS',
        'payload': {
            'salt': random_salt()
        }
    })


@log_request
def complete_signup(request):
    try:
        username = str(request.POST['username'])
        password_hash = str(request.POST['password_hash'])
        salt = str(request.POST['salt'])
        email = str(request.POST['email'])
    except (MultiValueDictKeyError, ValueError):
        return JsonResponse(common_response.INVALID_REQUEST_RESPONSE)

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

    new_user = User.objects.create(
        username=username,
        password_hash=password_hash,
        email=email,
        salt=salt,
        created_at=int(time.time()),
        modified_at=int(time.time())
    )

    return JsonResponse({
        'status': 'SUCCESS',
        'payload': {
            'user': {
                'user_id': new_user.id,
                'username': new_user.username,
                'email': new_user.email,
                'password_hash': password_hash,
                'salt': salt,
                'created_at': new_user.created_at,
                'modified_at': new_user.modified_at
            }
        }
    })


@log_request
def login(request):
    try:
        username = str(request.POST['username'])
        user = User.objects.get(username=username)
    except (ValueError, MultiValueDictKeyError):
        return JsonResponse(common_response.INVALID_REQUEST_RESPONSE)
    except models.ObjectDoesNotExist:
        return JsonResponse(common_response.USERNAME_NOT_FOUND_RESPONSE)

    return JsonResponse({
        'status': 'SUCCESS',
        'payload': {
            'salt': user.salt
        }
    })


@log_request
def complete_login(request):
    try:
        username = str(request.POST['username'])
        password_hash = str(request.POST['password_hash'])
    except (MultiValueDictKeyError, ValueError):
        return JsonResponse(common_response.INVALID_REQUEST_RESPONSE)

    if not validate_username(username):
        return JsonResponse(common_response.INVALID_USERNAME_RESPONSE)

    if not validate_password_hash(password_hash):
        return JsonResponse(common_response.INVALID_REQUEST_RESPONSE)

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
        'status': 'SUCCESS',
        'payload': {
            'session_id': session_id
        }
    })

    res.set_cookie('session_id', session_id, httponly=True)

    return res

