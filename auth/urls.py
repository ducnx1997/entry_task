from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^signup', views.signup),
    url(r'^complete_signup', views.complete_signup),
    url(r'^login', views.login),
    url(r'^complete_login$', views.complete_login),
]
