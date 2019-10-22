# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging
import time

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.paginator import Paginator
from django.db import models
from django.http import JsonResponse
from django.utils.datastructures import MultiValueDictKeyError

from auth import login_required, log_request
from ..common import common_response
from ..models import Event, User, EventImage
import logging

log = logging.getLogger('entry_task')


@log_request
@login_required
def get_event(request, user, event_id):
    try:
        event_id = int(event_id)
        event = Event.objects.get(id=event_id)
    except ValueError:
        return JsonResponse(common_response.INVALID_REQUEST_RESPONSE)
    except models.ObjectDoesNotExist:
        return JsonResponse(common_response.EVENT_NOT_FOUND_RESPONSE)

    images = list(EventImage.objects.filter(event_id=event.id).values('image_path'))

    return JsonResponse({
        'status': 'SUCCESS',
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


@log_request
@login_required
def get_events(request, user, page_id=1):
    events = Event.objects

    try:
        page_id = int(page_id)
        if 'tag' in request.POST:
            events = events.filter(tag=request.POST['tag'])
        if 'start_date' in request.POST:
            events = events.filter(event_datetime__gte=int(request.POST['start_date']))
        if 'end_date' in request.POST:
            events = events.filter(event_datetime__lte=int(request.POST['end_date']))

        if 'start_date' in request.POST and 'end_date' in request.POST:
            if int(request.POST['end_date']) - int(request.POST['start_date']) > settings.MAX_EVENT_SEARCH_TIME_RANGE:
                return JsonResponse(common_response.INVALID_REQUEST_RESPONSE)
    except (ValueError, MultiValueDictKeyError):
        return JsonResponse(common_response.INVALID_REQUEST_RESPONSE)

    events = events.order_by('-event_datetime')
    events = Paginator(events, settings.NUM_OF_EVENTS_PER_PAGE)

    if page_id > events.num_pages:
        page_id = 1

    events = events.page(page_id).object_list.values('id', 'title', 'event_datetime')

    events = list(events)

    # events = map(lambda x: model_to_dict(x), events)
    return JsonResponse({
        'status': 'SUCCESS',
        'payload': events
    })


@log_request
@login_required
def create_event(request, user):
    user = User.objects.get(id=user['id'])

    if not user.is_admin:
        return JsonResponse(common_response.NOT_AUTHORIZED)

    try:
        title = str(request.POST['title'])
        description = str(request.POST['description'])
        event_datetime = int(request.POST['event_datetime'])
        tag = str(request.POST['tag'])
        files = request.FILES.getlist('img')
    except (ValueError, MultiValueDictKeyError) as e:
        print(1)
        print(request.POST['title'])
        print(e)
        return JsonResponse(common_response.INVALID_REQUEST_RESPONSE)

    new_event = Event.objects.create(
        title=title,
        description=description,
        event_datetime=event_datetime,
        tag=tag,
        created_at=time.time(),
        modified_at=time.time()
    )

    event_image_paths = []

    for i in range(len(files)):
        if files[i].content_type == 'image/jpeg':
            image_path = str(str(int(new_event.id)) + '_' + str(i) + '.jpeg')

            default_storage.save(image_path, ContentFile(files[i].read()))

            EventImage.objects.create(
                event_id=new_event.id,
                image_path=image_path,
                created_at=time.time(),
                modified_at=time.time()
            )
            event_image_paths.append(image_path)

    return JsonResponse({
        'status': 'SUCCESS',
        'payload': {
            'event': {
                'id': new_event.id,
                'title': new_event.title,
                'description': new_event.description,
                'event_datetime': int(new_event.event_datetime),
                'tag': new_event.tag,
                'images': event_image_paths
            }
        }
    })
