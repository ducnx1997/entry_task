# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import time

from django.db import models
from django.http import JsonResponse

from common import common_response, user_action
from common.auth import login_required, log_request
from ..models import Event, Like, Activities


@log_request
@login_required
def get_likes(request, user, event_id):
    try:
        event = Event.objects.get(id=event_id)
    except models.ObjectDoesNotExist:
        return JsonResponse(common_response.EVENT_NOT_FOUND_RESPONSE)

    likes = Like.objects.filter(event_id=event_id)\
        .values('event_id', 'user_id', 'username', 'created_at')

    likes = list(likes)

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
    try:
        event = Event.objects.get(id=event_id)
    except models.ObjectDoesNotExist:
        return JsonResponse(common_response.EVENT_NOT_FOUND_RESPONSE)

    try:
        like = Like.objects.get(
            event_id=event_id,
            user_id=user['id']
        )
    except models.ObjectDoesNotExist:
        cur_time = time.time()

        like = Like.objects.create(
            event_id=event.id,
            user_id=user['id'],
            username=user['username'],
            created_at=cur_time,
            modified_at=cur_time
        )
        Activities.objects.update_or_create(
            action=user_action.LIKE,
            event_id=like.event_id,
            event_title=event.title,
            user_id=like.user_id,
            details='',
            created_at=cur_time,
            modified_at=cur_time
        )

    return JsonResponse({
        'status': common_response.SUCCESS_STATUS,
        'payload': {
            'event_id': event.id,
            'user_id': like.user_id,
            'username': like.username,
            'created_at': like.created_at
        }
    })
