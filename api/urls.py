from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^signup', views.signup, name='signup'),
    url(r'^complete_signup', views.complete_signup, name='complete_signup'),
    url(r'^login', views.login, name='login'),
    url(r'^complete_login$', views.complete_login, name='complete_login'),
    url(r'^event/(?P<event_id>[0-9]+)$', views.get_event, name='get_event'),
    url(r'^create_event$', views.create_event, name='create_event'),
    url(r'^get_events$', views.get_events, name='get_events'),
    url(r'^get_events/page/(?P<page_id>[0-9]+)$', views.get_events, name='get_events'),
    url(r'^event/(?P<event_id>[0-9]+)/like$', views.like_event, name='like_event'),
    url(r'^event/(?P<event_id>[0-9]+)/get_likes$', views.get_likes, name='get_likes'),
    url(r'^event/(?P<event_id>[0-9]+)/comment$', views.comment_event, name='comment_event'),
    url(r'^event/(?P<event_id>[0-9]+)/comments$', views.get_comments, name='get_comments'),
    url(r'^event/(?P<event_id>[0-9]+)/participate$', views.participate_event, name='participate_event'),
    url(r'^event/(?P<event_id>[0-9]+)/get_participants$', views.get_participants, name='get_participants')
]
