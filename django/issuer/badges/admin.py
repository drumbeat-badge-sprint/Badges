'''
Created on Apr 14, 2011

@author: Mike_Edwards
'''
from django.contrib import admin
from badges.models import Issuer, Badge, BadgeIssue, BadgeClaim, BadgeRequest,\
    Offering



admin.site.register(Issuer)
admin.site.register(Badge)
admin.site.register(BadgeRequest)
admin.site.register(BadgeIssue)
admin.site.register(BadgeClaim)
admin.site.register(Offering)