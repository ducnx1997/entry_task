# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import hashlib
import time
from functools import wraps

from django.conf import settings
from django.core.cache import cache
from django.db import models
from django.http import JsonResponse
from django.utils.datastructures import MultiValueDictKeyError
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from ..common import validate_username, common_response, random_salt, validate_password_hash, \
    validate_salt, random_session
from ..models import User

import logging


log = logging.getLogger('entry_task')


def login_required(view_function):

    @wraps(view_function)
    def wrap(*args, **kwargs):
        request = args[0]
        log.info(request)
        if 'session_id' not in request.COOKIES:
            return JsonResponse(common_response.LOGIN_REQUIRED)

        user = cache.get(request.COOKIES.get('session_id'))
        if user:
            log.info('user {} logged in'.format(user.id))
            return view_function(*args, user=user, **kwargs)

        return JsonResponse(common_response.LOGIN_REQUIRED)

    return wrap


def signup(request):
    try:
        username = str(request.POST['username'])
    except (MultiValueDictKeyError, ValueError):
        return JsonResponse(common_response.INVALID_REQUEST_RESPONSE)

    if not validate_username(username):
        return JsonResponse(common_response.INVALID_REQUEST_RESPONSE)

    if User.objects.filter(username=username).exists():
        return JsonResponse(common_response.USERNAME_EXISTS_RESPONSE)

    return JsonResponse({
        'status': 'SUCCESS',
        'payload': {
            'salt': random_salt()
        }
    })


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
    password_hash = hashlib.md5(username + salt).hexdigest()

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
                'password_hash': password_hash,
                'salt': salt,
                'created_at': new_user.created_at,
                'modified_at': new_user.modified_at
            }
        }
    })


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
        settings.SESSION_TIMEOUT
    )

    return JsonResponse({
        'status': 'SUCCESS',
        'payload': {
            'session_id': session_id
        }
    })
