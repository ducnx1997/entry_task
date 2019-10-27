# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.http import JsonResponse

from common import common_response
from common.auth import login_required, log_request
from common.modelmanager import CommentManager
from common.models import CommentTab
from common.validator import validate_schema


@log_request
@login_required
def get_comments(request, user, event_id, page=1):
    page = int(page)
    comments = CommentManager.get_comments(event_id=event_id, page=page)

    comments = list(comments.values('username', 'user_id', 'body', 'created_at'))

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
def comment_event(request, user, form_data, event_id):
    new_comment = CommentManager.create_comment(
        event_id=event_id,
        username=user['username'],
        user_id=user['id'],
        body=form_data['body']
    )

    return JsonResponse({
        'status': common_response.SUCCESS_STATUS,
        'payload': {
            'event_id': new_comment.event_id,
            'user_id': new_comment.user_id,
            'username': new_comment.username,
            'body': new_comment.body,
            'created_at': new_comment.created_at
        }
    })
