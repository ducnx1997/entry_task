from django.conf.urls import url

import views

urlpatterns = [
    url(r'^create_event$', views.create_event)
]
