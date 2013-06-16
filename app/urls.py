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
    url(r'^(?P<store_name>\w+)/add_to_cart/(?P<product_id>\d+)/$', views.cart, name='add_to_cart'),
    url(r'^(?P<store_name>\w+)/cart/$', views.cart, name='cart'),
    url(r'^(?P<store_name>\w+)/checkout_cart/$', views.checkout_cart, name='checkout_cart'),
)

