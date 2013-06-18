from django.conf.urls import patterns, url

from stores import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^add_to_cart/(?P<product_id>\d+)/$', views.cart, name='add_to_cart'),
    url(r'^remove_from_cart/(?P<product_id>\d+)/$', views.remove_from_cart, name='remove_from_cart'),
    url(r'^cart/$', views.cart, name='cart'),
    url(r'^checkout_cart/$', views.checkout_cart, name='checkout_cart'),
    url(r'^confirm_order/(?P<order_id>\d+)/$', views.confirm_order, name='confirm_order'),
    url(r'^delete_order/(?P<order_id>\d+)/$', views.delete_order, name='delete_order'),
    url(r'^past_orders/$', views.past_orders, name='past_orders'),
)

