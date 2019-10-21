# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.http import JsonResponse

from auth import login_required
from ..common import common_response
from ..models import User, Activities


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
