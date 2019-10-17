# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import time

from django.db import models
from django.http import JsonResponse

from auth import login_required
from ..common import common_response
from ..models import Event, Activities, Participation


@login_required
def get_participants(request, user, event_id):
    try:
        event_id = int(event_id)
        event = Event.objects.get(id=event_id)
    except ValueError:
        return JsonResponse(common_response.INVALID_REQUEST_RESPONSE)
    except models.ObjectDoesNotExist:
        return JsonResponse(common_response.EVENT_NOT_FOUND_RESPONSE)

    participants = list(Participation.objects.filter(event_id=event_id).values('user_id', 'created_at'))

    return JsonResponse(
        {
            'status': 'SUCCESS',
            'payload': {
                'participants': participants
            }
        }
    )


@login_required
def participate_event(request, user, event_id):
    try:
        event_id = int(event_id)
        event = Event.objects.get(id=event_id)
    except ValueError:
        return JsonResponse(common_response.INVALID_REQUEST_RESPONSE)
    except models.ObjectDoesNotExist:
        return JsonResponse(common_response.EVENT_NOT_FOUND_RESPONSE)

    try:
        participation = Participation.objects.get(
            event_id=event_id,
            user_id=user['id']
        )
    except models.ObjectDoesNotExist:
        participation = Participation.objects.create(
            event_id=event.id,
            user_id=user['id'],
            created_at=time.time(),
            modified_at=time.time()
        )
        Activities.objects.update_or_create(
            action='PARTICIPATION',
            event_id=participation.event_id,
            user_id=participation.user_id,
            details='',
            created_at=time.time(),
            modified_at=time.time()
        )

    return JsonResponse({
        'status': 'SUCCESS',
        'payload': {
            'event_id': participation.event_id,
            'user_id': participation.user_id,
            'created_at': participation.created_at,
            'modified_at': participation.modified_at
        }
    })

