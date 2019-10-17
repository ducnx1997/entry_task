# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import time

from django.db import models
from django.http import JsonResponse
from django.utils.datastructures import MultiValueDictKeyError

from auth import login_required
from ..common import common_response
from ..models import Event, Comment, Activities


@login_required
def get_comments(request, user, event_id):
    try:
        event_id = int(event_id)
        event = Event.objects.get(id=event_id)
    except ValueError:
        return JsonResponse(common_response.INVALID_REQUEST_RESPONSE)
    except models.ObjectDoesNotExist:
        return JsonResponse(common_response.EVENT_NOT_FOUND_RESPONSE)

    comments = list(Comment.objects.filter(event_id=event_id).values('id', 'user_id', 'created_at', 'body'))

    return JsonResponse(
        {
            'status': 'SUCCESS',
            'payload': {
                'message': comments
            }
        }
    )


@login_required
def comment_event(request, user, event_id):
    try:
        event_id = int(event_id)
        comment_body = str(request.POST['body'])
        event = Event.objects.get(id=event_id)
    except (ValueError, MultiValueDictKeyError):
        return JsonResponse(common_response.INVALID_REQUEST_RESPONSE)
    except models.ObjectDoesNotExist:
        return JsonResponse(common_response.EVENT_NOT_FOUND_RESPONSE)

    new_comment = Comment.objects.create(
        event_id=event.id,
        user_id=user['id'],
        body=comment_body,
        created_at=time.time(),
        modified_at=time.time()
    )

    Activities.objects.create(
        event_id=event.id,
        user_id=user['id'],
        details=new_comment.body,
        action='COMMENT',
        created_at=time.time(),
        modified_at=time.time()
    )

    return JsonResponse({
        'status': 'SUCCESS',
        'payload': {
            'event_id': new_comment.event_id,
            'user_id': new_comment.user_id,
            'body': new_comment.body,
            'created_at': new_comment.created_at
        }
    })
