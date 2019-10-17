# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import time

from django.core.cache import cache
from django.core import serializers
from django.forms.models import model_to_dict
from django.shortcuts import render
from django.http import JsonResponse
from django.utils.datastructures import MultiValueDictKeyError
from django.conf import settings
from django.db import models
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.core.paginator import Paginator

import logging

from ..models import Event, Like, Comment, User
from ..common import common_response, get_user
from auth import login_required


def get_user_activities(request, user_id):
    pass


def get_user_event(request, user_id):
    pass
