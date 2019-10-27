from django.conf.urls import url

import views

urlpatterns = [
    url(r'^user$', views.get_user_info),
    url(r'^user/(?P<target_id>[0-9]+)/activities$', views.get_user_activities),
    url(r'^event/(?P<event_id>[0-9]+)$', views.get_event),
    url(r'^events$', views.get_events),
    url(r'^events/page/(?P<page>[0-9]+)$', views.get_events),
    url(r'^event/(?P<event_id>[0-9]+)/like$', views.like_event),
    url(r'^event/(?P<event_id>[0-9]+)/likes$', views.get_likes),
    url(r'^event/(?P<event_id>[0-9]+)/likes/page/(?P<page>[0-9]+)$', views.get_likes),
    url(r'^event/(?P<event_id>[0-9]+)/comment$', views.comment_event),
    url(r'^event/(?P<event_id>[0-9]+)/comments$', views.get_comments),
    url(r'^event/(?P<event_id>[0-9]+)/comments/page/(?P<page>[0-9]+)$', views.get_comments),
    url(r'^event/(?P<event_id>[0-9]+)/participate$', views.participate_event),
    url(r'^event/(?P<event_id>[0-9]+)/participants$', views.get_participants)
]
