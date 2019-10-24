# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import time

from django.db import models
from django.http import JsonResponse
from django.utils.datastructures import MultiValueDictKeyError

from common.auth import login_required, log_request
from common import common_response, user_action
from common.validator import validate_schema
from ..models import Event, Comment, Activities


@log_request
@login_required
def get_comment(request, user, comment_id):
    try:
        comment = Comment.objects.get(id=comment_id)
    except models.ObjectDoesNotExist:
        return JsonResponse(common_response.EVENT_NOT_FOUND_RESPONSE)

    return JsonResponse({
        'status': common_response.SUCCESS_STATUS,
        'payload': {
            'event_id': comment.event_id,
            'comment_id': comment_id,
            'body': comment.body,
            'user_id': user['id'],
            'username': user['username']
        }
    })


@log_request
@login_required
def get_comments(request, user, event_id):
    try:
        event = Event.objects.get(id=event_id)
    except models.ObjectDoesNotExist:
        return JsonResponse(common_response.EVENT_NOT_FOUND_RESPONSE)

    comments = Comment.objects.filter(event_id=event_id)\
        .values('id', 'user_id', 'created_at', 'body', 'username', 'user_id')

    comments = list(comments)

    return JsonResponse(
        {
            'status': common_response.SUCCESS_STATUS,
            'payload': {
                'message': comments
            }
        }
    )


comment_form = {
    'type': 'object',
    'properties': {
        'body': {'type': 'string'}
    },
    'required': ['body']
}


@log_request
@validate_schema(schema=comment_form)
@login_required
def comment_event(request, user, event_id):
    try:
        event = Event.objects.get(id=event_id)
    except models.ObjectDoesNotExist:
        return JsonResponse(common_response.EVENT_NOT_FOUND_RESPONSE)

    cur_time = time.time()

    new_comment = Comment.objects.create(
        event_id=event.id,
        user_id=user['id'],
        username=user['username'],
        body=request.POST['body'],
        created_at=cur_time,
        modified_at=cur_time
    )

    Activities.objects.create(
        event_id=event.id,
        event_title=event.title,
        user_id=user['id'],
        details=new_comment.body,
        action=user_action.COMMENT,
        created_at=cur_time,
        modified_at=cur_time
    )

    return JsonResponse({
        'status': common_response.SUCCESS_STATUS,
        'payload': {
            'event_id': new_comment.event_id,
            'event_title': event.title,
            'user_id': new_comment.user_id,
            'username': new_comment.username,
            'body': new_comment.body,
            'created_at': new_comment.created_at
        }
    })
