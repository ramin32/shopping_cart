from django.conf.urls import patterns, url

from app import views

urlpatterns = patterns('',
    # user management
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.login, name='logout'),
    url(r'^register/$', views.register, name='register'),

    # store
    url(r'^$', views.index, name='index'),
    url(r'^(?P<store_name>\w+)/$', views.store, name='store'),
)

