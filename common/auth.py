# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging
from functools import wraps

from django.core.cache import cache
from django.http import JsonResponse

from common import common_response

log = logging.getLogger('entry_task')


def login_required(view_function):

    @wraps(view_function)
    def wrap(*args, **kwargs):
        request = args[0]
        if 'session_id' not in request.COOKIES:
            return JsonResponse(common_response.LOGIN_REQUIRED)

        user = cache.get(request.COOKIES.get('session_id'))
        if user:
            return view_function(*args, user=user, **kwargs)

        return JsonResponse(common_response.LOGIN_REQUIRED)

    return wrap


def log_request(view_function):
    @wraps(view_function)
    def wrap(*args, **kwargs):
        log.info('{}|COOKIES:{}|POST:{}'.format(args[0], args[0].COOKIES, args[0].POST))
        return view_function(*args, **kwargs)

    return wrap
