# -*- coding: utf-8 -*-
from __future__ import unicode_literals


SUCCESS_STATUS = 'SUCCESS'

INVALID_USERNAME_RESPONSE = {
    'status': 'INVALID_USERNAME'
}

INVALID_EMAIL_RESPONSE = {
    'status': 'INVALID_EMAIL'
}

USERNAME_EXISTS_RESPONSE = {
    'status': 'USERNAME_EXISTS'
}

EMAIL_USED_RESPONSE = {
    'status': 'EMAIL_ALREADY_USED'
}

USERNAME_NOT_FOUND_RESPONSE = {
    'status': 'USERNAME_NOT_FOUND'
}

WRONG_PASSWORD_RESPONSE = {
    'status': 'WRONG_PASSWORD'
}

EVENT_NOT_FOUND_RESPONSE = {
    'status': 'EVENT_NOT_FOUND'
}

INVALID_REQUEST_RESPONSE = {
    'status': 'INVALID_REQUEST'
}

LOGIN_REQUIRED = {
    'status': 'LOGIN_REQUIRED'
}

NOT_AUTHORIZED = {
    'status': 'NOT_AUTHORIZED'
}
