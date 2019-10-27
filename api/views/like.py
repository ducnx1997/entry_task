# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import JsonResponse

from common import common_response
from common.auth import login_required, log_request
from common.modelmanager import LikeManager


@log_request
@login_required
def get_likes(request, user, event_id, page=1):
    page = int(page)
    likes = LikeManager.get_likes(
        event_id=event_id,
        page=page
    )

    likes = list(likes.values('user_id', 'user_id', 'created_at'))

    return JsonResponse(
        {
            'status': common_response.SUCCESS_STATUS,
            'payload': {
                'likes': likes
            }
        }
    )


@log_request
@login_required
def like_event(request, user, event_id):
    new_like = LikeManager.create_like(
        user_id=user['id'],
        username=user['username'],
        event_id=event_id
    )

    return JsonResponse({
        'status': common_response.SUCCESS_STATUS,
        'payload': {
            'event_id': new_like.event_id,
            'user_id': new_like.user_id,
            'username': new_like.username,
            'created_at': new_like.created_at
        }
    })
