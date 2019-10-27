# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import JsonResponse

from common import common_response
from common.auth import login_required, log_request
from common.modelmanager import ParticipationManager


@log_request
@login_required
def get_participants(request, user, event_id, page=1):
    page = int(page)
    participants = ParticipationManager.get_participants(event_id=event_id, page=page)

    participants = list(participants.values('user_id', 'username', 'created_at'))

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
    participation = ParticipationManager.create_participation(
        user_id=user['id'],
        username=user['username'],
        event_id=event_id)

    return JsonResponse({
        'status': common_response.SUCCESS_STATUS,
        'payload': {
            'event_id': participation.event_id,
            'user_id': participation.user_id,
            'username': participation.username,
            'created_at': participation.created_at
        }
    })
