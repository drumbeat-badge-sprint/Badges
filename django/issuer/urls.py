from django.conf.urls.defaults import *
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

media_url = settings.MEDIA_URL.lstrip('/').rstrip('/')

urlpatterns = patterns('',
    (r'', include('dashboard.urls')),
    (r'^badges/', include('badges.urls')),
    (r'^openid/', include('openid_provider.urls')),
    (r'^accounts/', include('registration.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^%s/(?P<path>.*)$' % media_url, 'django.views.static.serve',
     { 'document_root': settings.MEDIA_ROOT }),
)
