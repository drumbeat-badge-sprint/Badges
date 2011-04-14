from django.contrib.auth.models import User
from django.contrib import admin
from django.db import models

from openid_provider.models import OpenID
import settings
import calendar

try:
    import json
except ImportError:
    import simplejson as json

class Badge(models.Model):
    title = models.CharField(max_length=125)
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return '/badges/%d' % (self.pk,)

class BadgeIssue(models.Model):
    user = models.ForeignKey(User,related_name="issues")
    badge = models.ForeignKey(Badge,related_name="issues")
    timestamp = models.DateTimeField(auto_now_add=True)
    issuer = models.URLField()

class BadgeClaim(models.Model):
    issue = models.ForeignKey(BadgeIssue,related_name="claims")
    timestamp = models.DateTimeField(auto_now_add=True)

    def json(self):
        return json.dumps(self.serialized())

    def serialized(self):
        openid = OpenID.objects.get(user=self.user)
        return {
            'schema': 'http://example.org/badge/%d' % (self.issue.badge.pk,),
            'mustSupport': [],
            'title': self.issue.badge.title,
            'description': self.issue.badge.description,
            'timestamp': calendar.timegm(self.timestamp.timetuple()),
            'issuer': self.issue.issuer,
            'badgeURL': settings.HOST_SERVER + self.issue.badge.get_absolute_url(),
            'issuee': [
                {
                    'type': 'openid',
                    'id': settings.HOST_SERVER + '/openid/%s/' % (openid.openid,),
                },
                {
                    'type': 'email',
                    'id': self.issue.user.email
                }
            ],
        }


admin.site.register(Badge)
admin.site.register(BadgeIssue)
admin.site.register(BadgeClaim)
