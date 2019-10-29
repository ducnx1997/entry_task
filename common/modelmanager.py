# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import time

from django.core.exceptions import ObjectDoesNotExist
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.paginator import Paginator
from django.db import IntegrityError

from common import constant
from common import user_action
from common.models import UserTab, ActivitiesTab, ParticipationTab, EventTab, EventImageMappingTab, LikeTab, CommentTab


class UserManager(object):

    @staticmethod
    def get_user_by_id(user_id=None):
        try:
            user = UserTab.objects.get(id=user_id)
            return user
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def get_user_by_username(username=None):
        try:
            user = UserTab.objects.get(username=username)
            return user
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def get_user_by_email(email=None):
        try:
            user = UserTab.objects.get(email=email)
            return user
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def create_user(username, email, password_hash, salt):
        try:
            cur_time = time.time()
            user = UserTab.objects.create(
                username=username,
                email=email,
                password_hash=password_hash,
                salt=salt,
                created_at=cur_time,
                modified_at=cur_time
            )
            return user
        except IntegrityError:
            return None

    @staticmethod
    def get_user_activities(user_id=None, page=1, per_page=constant.NUM_OF_EVENTS_PER_PAGE):
        activities = ActivitiesTab.objects.filter(user_id=user_id).order_by('-created_at')
        paginated_activities = Paginator(activities, per_page)
        if page > paginated_activities.num_pages:
            page = 1
        return paginated_activities.page(page).object_list


class EventManager(object):

    @staticmethod
    def get_event_by_id(event_id):
        try:
            event = EventTab.objects.get(id=event_id)
            return event
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def get_event_images(event_id):
        return EventImageMappingTab.objects.filter(event_id=event_id)

    @staticmethod
    def get_events(tag=None, start_date=None, end_date=None, page=1, per_page=constant.NUM_OF_EVENTS_PER_PAGE):
        if tag and start_date and end_date:
            events = EventTab.objects.filter(
                tag=tag,
                event_datetime__gte=start_date,
                event_datetime__lte=end_date)
        elif tag:
            events = EventTab.objects.filter(tag=tag)
        elif start_date and end_date:
            events = EventTab.objects.filter(
                event_datetime__gte=start_date,
                event_datetime__lte=end_date)
        else:
            events = EventTab.objects

        events = events.order_by('-event_datetime')
        paginated_events = Paginator(events, per_page)

        if page > paginated_events.num_pages:
            page = 1

        return paginated_events.page(page).object_list

    @staticmethod
    def create_event(title, description, event_datetime, tag, files):
        cur_time = time.time()

        new_event = EventTab.objects.create(
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

                EventImageMappingTab.objects.create(
                    event_id=new_event.id,
                    image_path=image_path,
                    created_at=cur_time,
                    modified_at=cur_time
                )
                event_image_paths.append(image_path)

        return new_event, event_image_paths


class ParticipationManager(object):
    @staticmethod
    def get_participants(event_id, page=1, per_page=constant.NUM_OF_EVENTS_PER_PAGE):
        participants = ParticipationTab.objects.filter(event_id=event_id)
        participants = Paginator(participants, per_page)

        if page > participants.num_pages:
            page = 1

        return participants.page(page).object_list

    @staticmethod
    def create_participation(user_id, username, event_id):
        try:
            event = EventTab.objects.get(id=event_id)
        except ObjectDoesNotExist:
            return None

        try:
            participation = ParticipationTab.objects.get(
                event_id=event_id,
                user_id=user_id
            )
        except ObjectDoesNotExist:
            cur_time = time.time()
            try:
                participation = ParticipationTab.objects.create(
                    event_id=event.id,
                    user_id=user_id,
                    username=username,
                    created_at=cur_time,
                    modified_at=cur_time
                )
                ActivitiesTab.objects.create(
                    action=user_action.PARTICIPATE,
                    event_id=participation.event_id,
                    event_title=event.title,
                    user_id=participation.user_id,
                    details='',
                    created_at=cur_time,
                    modified_at=cur_time
                )
            except IntegrityError:
                participation = ParticipationTab.objects.get(event_id=event_id, user_id=user_id)

        return participation


class LikeManager(object):

    @staticmethod
    def get_likes(event_id, page=1, per_page=constant.NUM_OF_EVENTS_PER_PAGE):
        likes = LikeTab.objects.filter(event_id=event_id).order_by('-created_at')
        likes = Paginator(likes, per_page)

        if page > likes.num_pages:
            page = 1

        return likes.page(page).object_list

    @staticmethod
    def create_like(user_id, username, event_id):
        try:
            event = EventTab.objects.get(id=event_id)
        except ObjectDoesNotExist:
            return None

        try:
            like = LikeTab.objects.get(
                event_id=event_id,
                user_id=user_id
            )
        except ObjectDoesNotExist:
            cur_time = time.time()
            try:
                like = LikeTab.objects.create(
                    event_id=event.id,
                    user_id=user_id,
                    username=username,
                    created_at=cur_time,
                    modified_at=cur_time
                )
                ActivitiesTab.objects.update_or_create(
                    action=user_action.LIKE,
                    event_id=like.event_id,
                    event_title=event.title,
                    user_id=like.user_id,
                    details='',
                    created_at=cur_time,
                    modified_at=cur_time
                )
            except IntegrityError:
                like = LikeTab.objects.create(
                    event_id=event_id,
                    user_id=user_id
                )

        return like


class CommentManager(object):

    @staticmethod
    def get_comments(event_id, page=1, per_page=constant.NUM_OF_EVENTS_PER_PAGE):
        comments = CommentTab.objects.filter(event_id=event_id).order_by('-created_at')
        comments = Paginator(comments, per_page)

        if page > comments.num_pages:
            page = 1

        return comments.page(page).object_list

    @staticmethod
    def create_comment(event_id, user_id, username, body=''):
        try:
            event = EventTab.objects.get(id=event_id)
        except ObjectDoesNotExist:
            return None

        cur_time = time.time()

        new_comment = CommentTab.objects.create(
            event_id=event.id,
            user_id=user_id,
            username=username,
            body=body,
            created_at=cur_time,
            modified_at=cur_time
        )

        ActivitiesTab.objects.create(
            event_id=event.id,
            event_title=event.title,
            user_id=user_id,
            details=new_comment.body,
            action=user_action.COMMENT,
            created_at=cur_time,
            modified_at=cur_time
        )

        return new_comment
