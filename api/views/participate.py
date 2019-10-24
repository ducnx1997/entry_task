# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import time

from django.db import models
from django.http import JsonResponse

from common.auth import login_required, log_request
from common import common_response, user_action
from ..models import Event, Activities, Participation


@log_request
@login_required
def get_participants(request, user, event_id):
    try:
        event = Event.objects.get(id=event_id)
    except models.ObjectDoesNotExist:
        return JsonResponse(common_response.EVENT_NOT_FOUND_RESPONSE)

    participants = Participation.objects.filter(event_id=event_id)\
        .values('user_id', 'created_at', 'username')

    participants = list(participants)

    return JsonResponse(
        {
            'status': common_response.SUCCESS_STATUS,
            'payload': {
                'participants': participants
            }
        }
    )


@log_request
@login_required
def participate_event(request, user, event_id):
    try:
        event = Event.objects.get(id=event_id)
    except models.ObjectDoesNotExist:
        return JsonResponse(common_response.EVENT_NOT_FOUND_RESPONSE)

    try:
        participation = Participation.objects.get(
            event_id=event_id,
            user_id=user['id']
        )
    except models.ObjectDoesNotExist:
        cur_time = time.time()
        participation = Participation.objects.create(
            event_id=event.id,
            user_id=user['id'],
            username=user['username'],
            created_at=cur_time,
            modified_at=cur_time
        )
        Activities.objects.update_or_create(
            action=user_action.PARTICIPATE,
            event_id=participation.event_id,
            event_title=event.title,
            user_id=participation.user_id,
            details='',
            created_at=cur_time,
            modified_at=cur_time
        )

    return JsonResponse({
        'status': common_response.SUCCESS_STATUS,
        'payload': {
            'event_id': participation.event_id,
            'user_id': participation.user_id,
            'username': participation.username,
            'created_at': participation.created_at
        }
    })
