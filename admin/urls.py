from django.conf.urls import url

import views

urlpatterns = [
    url(r'^create_event$', views.create_event),
    url(r'^login_template$', views.login_template),
    url(r'^create_event_template$', views.create_event_template)
]
