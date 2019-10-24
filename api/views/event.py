# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging
import time

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.paginator import Paginator
from django.db import models
from django.http import JsonResponse

import constant
from common import common_response
from common.auth import login_required, log_request
from common.validator import validate_schema
from ..models import Event, User, EventImage

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
            'type': 'string',
            "pattern": r'^\d+$'
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
def create_event(request, user):
    user = User.objects.get(id=user['id'])
    if not user.is_admin:
        return JsonResponse(common_response.NOT_AUTHORIZED)

    title = request.POST['title']
    description = request.POST['description']
    event_datetime = request.POST['event_datetime']
    tag = request.POST['tag']
    files = request.FILES.getlist('img')

    cur_time = time.time()

    new_event = Event.objects.create(
        title=title,
        description=description,
        event_datetime=event_datetime,
        tag=tag,
        created_at=cur_time,
        modified_at=cur_time
    )

    event_image_paths = []

    for i in range(len(files)):
        if files[i].content_type == 'image/jpeg':
            image_path = str(str(int(new_event.id)) + '_' + str(i) + '.jpeg')

            default_storage.save(image_path, ContentFile(files[i].read()))

            EventImage.objects.create(
                event_id=new_event.id,
                image_path=image_path,
                created_at=cur_time,
                modified_at=cur_time
            )
            event_image_paths.append(image_path)

    return JsonResponse({
        'status': common_response.SUCCESS_STATUS,
        'payload': {
            'event': {
                'id': new_event.id,
                'title': new_event.title,
                'description': new_event.description,
                'event_datetime': new_event.event_datetime,
                'tag': new_event.tag,
                'images': event_image_paths
            }
        }
    })


@log_request
@login_required
def get_event(request, user, event_id):
    try:
        event = Event.objects.get(id=event_id)
    except models.ObjectDoesNotExist:
        return JsonResponse(common_response.EVENT_NOT_FOUND_RESPONSE)

    images = list(EventImage.objects.filter(event_id=event.id).values('image_path'))

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
        'start_date': {'type': 'string', "pattern": r'^\d+$'},
        'end_date': {'type': 'string', "pattern": r'^\d+$'}
    }
}


@log_request
@validate_schema(get_events_form)
@login_required
def get_events(request, user, page_id=1):
    events = Event.objects

    if 'tag' in request.POST:
        events = events.filter(tag=request.POST['tag'])
    if 'start_date' in request.POST and 'end_date' in request.POST:
        if int(request.POST['end_date']) - int(request.POST['start_date']) > constant.MAX_EVENT_SEARCH_TIME_RANGE:
            return JsonResponse(common_response.INVALID_REQUEST_RESPONSE)
        events = events.filter(
            event_datetime__gte=int(request.POST['start_date']),
            eventevent_datetime__lte=int(request.POST['end_date']))
    elif 'start_date' in request.POST or 'end_date' in request.POST:
        return JsonResponse(common_response.INVALID_REQUEST_RESPONSE)

    events = events.order_by('-event_datetime')
    events = Paginator(events, constant.NUM_OF_EVENTS_PER_PAGE)

    if page_id > events.num_pages:
        page_id = 1

    events = events.page(page_id).object_list.values('id', 'title', 'event_datetime')

    events = list(events)

    return JsonResponse({
        'status': common_response.SUCCESS_STATUS,
        'payload': events
    })
