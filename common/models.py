# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class UserTab(models.Model):
    username = models.CharField(max_length=32)
    salt = models.CharField(max_length=8)
    email = models.CharField(max_length=128)
    password_hash = models.CharField(max_length=64)
    is_admin = models.BooleanField(default=False)
    created_at = models.BigIntegerField()
    modified_at = models.BigIntegerField()

    class Meta:
        db_table = 'user_tab'
        app_label = 'api'


class EventTab(models.Model):
    title = models.CharField(max_length=256)
    description = models.TextField()
    event_datetime = models.BigIntegerField()
    tag = models.CharField(max_length=256)
    created_at = models.BigIntegerField()
    modified_at = models.BigIntegerField()

    class Meta:
        db_table = 'event_tab'
        app_label = 'api'


class ParticipationTab(models.Model):
    event_id = models.BigIntegerField()
    user_id = models.BigIntegerField()
    username = models.CharField(max_length=32)
    created_at = models.BigIntegerField()
    modified_at = models.BigIntegerField()

    class Meta:
        db_table = 'participation_tab'
        app_label = 'api'


class EventImageMappingTab(models.Model):
    event_id = models.BigIntegerField()
    created_at = models.BigIntegerField()
    modified_at = models.BigIntegerField()
    image_path = models.CharField(max_length=256)

    class Meta:
        db_table = 'event_image_mapping_tab'
        app_label = 'api'


class LikeTab(models.Model):
    event_id = models.BigIntegerField()
    user_id = models.BigIntegerField()
    username = models.CharField(max_length=32)
    created_at = models.BigIntegerField()
    modified_at = models.BigIntegerField()

    class Meta:
        db_table = 'like_tab'
        app_label = 'api'


class CommentTab(models.Model):
    event_id = models.BigIntegerField()
    user_id = models.BigIntegerField()
    username = models.CharField(max_length=32)
    body = models.TextField()
    created_at = models.BigIntegerField()
    modified_at = models.BigIntegerField()

    class Meta:
        db_table = 'comment_tab'
        app_label = 'api'


class ActivitiesTab(models.Model):
    action = models.CharField(max_length=16)
    event_id = models.BigIntegerField()
    event_title = models.CharField(max_length=256)
    user_id = models.BigIntegerField()
    created_at = models.BigIntegerField()
    modified_at = models.BigIntegerField()
    details = models.TextField()

    class Meta:
        db_table = 'activities_tab'
        app_label = 'api'
