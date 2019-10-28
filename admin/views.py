# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

from django.http import JsonResponse
from django.template.loader import get_template
from django.template.response import TemplateResponse

from common import common_response, constant
from common.modelmanager import EventManager, UserManager
from common.auth import login_required, log_request
from common.validator import validate_schema

log = logging.getLogger('entry_task')


create_event_form = {
    'type': 'object',
    'properties': {
        'title': {
            'type': 'string',
            'minLength': 1,
            'maxLength': constant.MAX_EVENT_TITLE_LENGTH
        },
        'description': {'type': 'string'},
        'event_datetime': {
            'type': 'integer'
        },
        'tag': {
            'type': 'string',
            'minLength': 1,
            'maxLength': constant.MAX_TAG_LENGTH
        }
    },
    'required': ['title', 'description', 'event_datetime', 'tag']
}


@log_request
@validate_schema(schema=create_event_form)
@login_required
def create_event(request, user, form_data):
    user = UserManager.get_user_by_id(user['id'])
    if not user.is_admin:
        return JsonResponse(common_response.NOT_AUTHORIZED)

    title = form_data['title']
    description = form_data['description']
    event_datetime = form_data['event_datetime']
    tag = form_data['tag']
    files = request.FILES.getlist('img')

    new_event, event_image_paths = EventManager.create_event(title, description, event_datetime, tag, files)

    return JsonResponse({
        'status': common_response.SUCCESS_STATUS,
        'payload': {
            'event': {
                'id': new_event.id,
                'title': new_event.title,
                'description': new_event.description,
                'tag': new_event.tag,
                'event_datetime': new_event.event_datetime,
                'images': event_image_paths
            }
        }
    })


def get_login(request):

    return TemplateResponse(request, get_template('login.html'), {})
