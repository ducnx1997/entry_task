# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import time

from django.db import models
from django.http import JsonResponse

from auth import login_required
from ..common import common_response
from ..models import Event, Like, Activities


@login_required
def get_likes(request, user, event_id):
    try:
        event_id = int(event_id)
        event = Event.objects.get(id=event_id)
    except ValueError:
        return JsonResponse(common_response.INVALID_REQUEST_RESPONSE)
    except models.ObjectDoesNotExist:
        return JsonResponse(common_response.EVENT_NOT_FOUND_RESPONSE)

    likes = list(Like.objects.filter(event_id=event_id).values('user_id', 'created_at'))

    return JsonResponse(
        {
            'status': 'SUCCESS',
            'payload': {
                'likes': likes
            }
        }
    )


@login_required
def like_event(request, user, event_id):
    try:
        event_id = int(event_id)
        event = Event.objects.get(id=event_id)
    except ValueError:
        return JsonResponse(common_response.INVALID_REQUEST_RESPONSE)
    except models.ObjectDoesNotExist:
        return JsonResponse(common_response.EVENT_NOT_FOUND_RESPONSE)

    try:
        like = Like.objects.get(
            event_id=event_id,
            user_id=user['id']
        )
    except models.ObjectDoesNotExist:
        like = Like.objects.create(
            event_id=event.id,
            user_id=user['id'],
            created_at=time.time(),
            modified_at=time.time()
        )
        Activities.objects.update_or_create(
            action='LIKE',
            event_id=like.event_id,
            user_id=like.user_id,
            details='',
            created_at=time.time(),
            modified_at=time.time()
        )

    return JsonResponse({
        'status': 'SUCCESS',
        'payload': {
            'user_id': like.user_id,
            'created_at': like.created_at
        }
    })
