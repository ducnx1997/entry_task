from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^signup', views.signup, name='signup'),
    url(r'^complete_signup', views.complete_signup, name='complete_signup'),
    url(r'^login', views.login, name='login'),
    url(r'^complete_login$', views.complete_login, name='complete_login'),
    url(r'^user/(?P<target_id>[0-9]+)$', views.get_user_info, name='get_user_info'),
    url(r'^user/(?P<target_id>[0-9]+)/activities$', views.get_user_activities, name='get_user_activities'),
    url(r'^event/(?P<event_id>[0-9]+)$', views.get_event, name='get_event'),
    url(r'^create_event$', views.create_event, name='create_event'),
    url(r'^events$', views.get_events, name='get_events'),
    url(r'^get_events/page/(?P<page_id>[0-9]+)$', views.get_events, name='get_events'),
    url(r'^event/(?P<event_id>[0-9]+)/like$', views.like_event, name='like_event'),
    url(r'^event/(?P<event_id>[0-9]+)/likes$', views.get_likes, name='get_likes'),
    url(r'^event/(?P<event_id>[0-9]+)/comment$', views.comment_event, name='comment_event'),
    url(r'^comment/(?P<comment_id>[0-9]+)$', views.get_comment, name='get_comment'),
    url(r'^event/(?P<event_id>[0-9]+)/comments$', views.get_comments, name='get_comments'),
    url(r'^event/(?P<event_id>[0-9]+)/participate$', views.participate_event, name='participate_event'),
    url(r'^event/(?P<event_id>[0-9]+)/participants$', views.get_participants, name='get_participants')

]
