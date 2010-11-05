from django.contrib.auth.models import User
from django.contrib import admin
from django.db import models

from openid_provider.models import OpenID

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

class BadgeClaim(models.Model):
    user = models.ForeignKey(User)
    badge = models.ForeignKey(Badge)

    def json(self):
        return json.dumps(self.serialized())

    def serialized(self):
        openid = OpenID.objects.get(user=self.user)
        return {
            'schema': 'http://example.org/badge/%d' % (self.badge.pk,),
            'mustSupport': [],
            'title': self.badge.title,
            'description': self.badge.description,
            'timestamp': '123456',
            'issuer': 'http://www.drumbeat.org/',
            'badgeURL': 'http://localhost:8000' + self.badge.get_absolute_url(),
            'issuee': [
                {
                    'type': 'openid',
                    'id': 'http://localhost:8000/openid/%s/' % (openid.openid,),
                },
                {
                    'type': 'email',
                    'id': self.user.email
                }
            ],
        }


admin.site.register(Badge)
admin.site.register(BadgeClaim)
