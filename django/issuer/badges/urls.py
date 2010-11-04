from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^$', 'badges.views.index'),
    (r'^(?P<badge_id>[\d]+)/$', 'badges.views.badge'),
    (r'^claim/$', 'badges.views.claim'),
    (r'^drop/$', 'badges.views.drop'),
    (r'^(?P<username>[\w-]+)/$', 'badges.views.badges'),          
)
