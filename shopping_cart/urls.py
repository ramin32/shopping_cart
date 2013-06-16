from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import RedirectView
from django.core.urlresolvers import reverse

admin.autodiscover()

from stores.views import index

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),

    url(r'^users/', include('users.urls')),
    url(r'^stores/', include('stores.urls')),

    url(r'^$', index, name='index'),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
