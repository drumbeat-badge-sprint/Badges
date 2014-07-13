from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$', 'badges.views.index',name="badges_index"),
    
    url(r'^all/$', 'badges.views.badges',name="badges_badges"),
    #url(r'^add/$', 'badges.views.badge',name="badges_badge_add"),
    url(r'^(?P<badge_id>[\d]+)/$', 'badges.views.badge',name="badges_badge"),
    #url(r'^(?P<badge_id>[\d]+)/edit/$', 'badges.views.badge',name="badges_badge_edit"),
    
    url(r'^requests/$', 'badges.views.requests',name="badges_requests"),
    url(r'^request/(?P<issuer_id>[\d]+)/(?P<badge_id>[\d]+)/$', 'badges.views.request',name="badges_request"),
    
    url(r'^issue/$', 'badges.views.issue',name="badges_issue"),
    url(r'^claim/$', 'badges.views.claim',name="badges_claim"),
    url(r'^drop/$', 'badges.views.drop',name="badges_drop"),

    #url(r'^issuers/$', 'badges.views.issuers',name="badges_issuers"),
    url(r'^issuer/(?P<issuer_id>[\d]+)/$', 'badges.views.issuer',name="badges_issuer"),

    url(r'^api/user/(?P<username>[\w-]+)/$', 'badges.views.claims',name="badges_badges_user"),          
    url(r'^api/user/(?P<username>[\w-]+)/badges/$', 'badges.views.claims',name="badges_badges_user"), #alternate URL   
    url(r'^api/user/(?P<username>[\w-]+)/issues/$', 'badges.views.issues',name="badges_issues_user"),          
    url(r'^api/claim/$', 'badges.views.claim_json',name="badges_api_claim"),
    url(r'^api/request/$', 'badges.views.request_json',name="badges_api_request"),
)
