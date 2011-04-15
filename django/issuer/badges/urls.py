from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$', 'badges.views.index',name="badges_index"),
    url(r'^(?P<badge_id>[\d]+)/$', 'badges.views.badge',name="badges_badge"),
    url(r'^add/$', 'badges.views.badge',name="badges_badge_add"),
    url(r'^(?P<badge_id>[\d]+)/edit/$', 'badges.views.badge',name="badges_badge_edit"),
    url(r'^claim/$', 'badges.views.claim',name="badges_claim"),
    url(r'^drop/$', 'badges.views.drop',name="badges_drop"),
    url(r'^(?P<username>[\w-]+)/$', 'badges.views.badges',name="badges_badges_user"),          
    url(r'^(?P<username>[\w-]+)/badges/$', 'badges.views.badges',name="badges_badges_user"), #alternate URL   
    url(r'^(?P<username>[\w-]+)/issues/$', 'badges.views.issues',name="badges_issues_user"),          
)
