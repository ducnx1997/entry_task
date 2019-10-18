# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import time

from django.core.cache import cache
from django.core import serializers
from django.forms.models import model_to_dict
from django.shortcuts import render
from django.http import JsonResponse
from django.utils.datastructures import MultiValueDictKeyError
from django.conf import settings
from django.db import models
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.core.paginator import Paginator

import logging

from ..models import Event, Like, Comment, User, Activities
from ..common import common_response, get_user
from auth import login_required


@login_required
def get_user_info(request, user, target_id):
    try:
        user = User.objects.get(id=target_id)
    except models.ObjectDoesNotExist:
        return JsonResponse(common_response.USERNAME_NOT_FOUND_RESPONSE)

    return JsonResponse({
        'status': 'SUCCESS',
        'payload': {
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'created_at': user.created_at
            }
        }
    })


@login_required
def get_user_activities(request, user, target_id):
    activities = Activities.objects\
        .filter(user_id=user['id']).order_by('-created_at')\
        .values('action', 'event_id', 'event_title', 'user_id', 'details', 'created_at')

    activities = list(activities)

    return JsonResponse({
        'status': 'SUCCESS',
        'payload': activities
    })


# def get_user_event(request, user_id):
#     pass
