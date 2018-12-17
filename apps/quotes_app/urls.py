from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.login),
    url(r'^process_login$', views.process_login),
    url(r'^process$', views.process),
    url(r'^quotes$', views.quotes),
    url(r'^process_like$', views.process_like),
    url(r'^process_quote$', views.process_quote),
    url(r'^delete_quote$', views.delete_quote),
    url(r'^login$', views.login),
    url(r'^user/(?P<id>\d+)$', views.user),
    url(r'^myaccount/(?P<id>\d+)$', views.myaccount),
    url(r'^edit_user', views.edit_user),
    url(r'^logout$', views.logout),
]