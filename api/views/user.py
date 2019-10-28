# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import JsonResponse

from common import common_response
from common.auth import login_required, log_request
from common.modelmanager import UserManager


@log_request
@login_required
def get_user_info(request, user):
    user = UserManager.get_user_by_id(user_id=user['id'])
    if not user:
        return JsonResponse(common_response.USERNAME_NOT_FOUND_RESPONSE)

    return JsonResponse({
        'status': common_response.SUCCESS_STATUS,
        'payload': {
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'created_at': user.created_at
            }
        }
    })


@log_request
@login_required
def get_user_activities(request, user, target_id, page=1):
    activities = UserManager.get_user_activities(user_id=target_id, page=int(page))

    activities = list(activities.values(
        'action',
        'event_id',
        'event_title',
        'created_at',
        'details'))

    return JsonResponse({
        'status': common_response.SUCCESS_STATUS,
        'payload': activities
    })
