# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import base64
import hashlib
import logging
from functools import wraps

from Crypto import Random
from Crypto.Cipher import AES
from django.core.cache import cache
from django.http import JsonResponse

from common import common_response

log = logging.getLogger('entry_task')


class AESCipher(object):

    def __init__(self, key):
        self.bs = AES.block_size
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, raw):
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]


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
        # log.info('FILES:{}'.format(args[0].FILES.getlist('img')))
        return view_function(*args, **kwargs)

    return wrap
