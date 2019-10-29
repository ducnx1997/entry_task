# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging
import os

from PIL import Image
from django.conf import settings
from django.http import JsonResponse, HttpResponse

from common import common_response, constant
from common.auth import login_required, log_request
from common.modelmanager import EventManager
from common.validator import validate_schema

log = logging.getLogger('entry_task')


@log_request
@login_required
def get_event(request, user, event_id):
    event = EventManager.get_event_by_id(event_id)
    if not event:
        return JsonResponse(common_response.EVENT_NOT_FOUND_RESPONSE)
    images = list(EventManager.get_event_images(event_id=event_id).values('image_path'))

    return JsonResponse({
        'status': common_response.SUCCESS_STATUS,
        'payload': {
            'event': {
                'event_id': event.id,
                'description': event.description,
                'event_datetime': event.event_datetime,
                'tag': event.tag,
                'images': images
            }
        }
    })


get_events_form = {
    'type': 'object',
    'properties': {
        'tag': {
            'type': 'string',
            'minLength': 1,
            'maxLength': constant.MAX_TAG_LENGTH
        },
        'start_date': {
            'type': 'integer',
            'minimum': 0,
            'exclusiveMaximum': 9999999999
        },
        'end_date': {
            'type': 'integer',
            'minimum': 0,
            'exclusiveMaximum': 9999999999
        }
    }
}


@log_request
@validate_schema(get_events_form)
@login_required
def get_events(request, user, form_data, page=1):
    tag = form_data.get('tag')
    start_date = form_data.get('start_date')
    end_date = form_data.get('end_date')
    if start_date and end_date:
        if end_date - start_date > constant.MAX_EVENT_SEARCH_TIME_RANGE:
            start_date = end_date - constant.MAX_EVENT_SEARCH_TIME_RANGE
    events = EventManager.get_events(
        tag=tag,
        start_date=start_date,
        end_date=end_date,
        page=page
    )

    events = list(events.values(
        'title',
        'description',
        'event_datetime',
        'tag',
    ))

    return JsonResponse({
        'status': common_response.SUCCESS_STATUS,
        'payload': events
    })


get_image_form = {
    'type': 'object',
    'properties': {
        'path': {'type': 'string'}
    },
    'required': ['path']
}


@log_request
@validate_schema(get_events_form)
@login_required
def get_image(request, user, form_data):
    try:
        with open(os.path.join(settings.MEDIA_ROOT, form_data['path']), 'rb') as f:
            return HttpResponse(f.read(), content_type='image/jpeg')
    except IOError:
        red = Image.new('RGBA', (1, 1), (255, 0, 0, 0))
        response = HttpResponse(content_type="image/jpeg")
        red.save(response, "JPEG")
        return response
