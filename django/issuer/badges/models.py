from django.contrib.auth.models import User
from django.contrib import admin
from django.db import models

from openid_provider.models import OpenID
import settings
import calendar
import datetime

try:
    import json
except ImportError:
    import simplejson as json
    
class Issuer(models.Model):
    users = models.ManyToManyField(User,related_name="issuers")
    name = models.CharField(max_length=125)
    url = models.URLField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return self.name

class Badge(models.Model):
    title = models.CharField(max_length=125)
    description = models.TextField()
    image = models.ImageField(upload_to="badges/",null=True,blank=True)
    imageURL = models.URLField(null=True,blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return '/badges/%d' % (self.pk,)
    
    def __unicode__(self):
        return self.title

class BadgeIssue(models.Model):
    user = models.ForeignKey(User,related_name="issues")
    badge = models.ForeignKey(Badge,related_name="issues")
    timestamp = models.DateTimeField(auto_now_add=True)
    expires = models.DateTimeField(default=datetime.datetime(year=2100,month=12,day=31))
    issuer = models.ForeignKey(Issuer,related_name="issues")
    accepted = models.BooleanField(default=False)

    def __unicode__(self):
        return "%s issued %s to %s" % (self.issuer, self.badge, self.user)

class BadgeClaim(models.Model):
    issue = models.ForeignKey(BadgeIssue,related_name="claims")
    timestamp = models.DateTimeField(auto_now_add=True)

    def json(self):
        return json.dumps(self.serialized())

    def serialized(self):
        issuee = [
                {
                    'type': 'email',
                    'id': self.issue.user.email
                }
                ]
        
        try:
            openid = OpenID.objects.get(user=self.issue.user)
            issuee.append({
                                'type': 'openid',
                                'id': settings.HOST_SERVER + '/openid/%s/' % (openid.openid,),
                            })
                
        except OpenID.DoesNotExist:
            openid = None
            
        
        if self.issue.badge.image.name is not None:
            name = self.issue.badge.image.name
            image = self.issue.badge.image
            image_url = self.issue.badge.image.url
        else:
            image_url = self.issue.badge.imageURL
            
        s = settings
            
        return {
            'schema': 'http://example.org/badge/%d' % (self.issue.badge.pk,),
            'mustSupport': [],
            'title': self.issue.badge.title,
            'description': self.issue.badge.description,
            'timestamp': calendar.timegm(self.timestamp.timetuple()),
            'expires': calendar.timegm(self.issue.expires.timetuple()),
            'badgeURL': settings.HOST_SERVER + self.issue.badge.get_absolute_url(),
            'issuer': self.issue.issuer.url,
            'issuerName': self.issue.issuer.name,
            'imageURL': image_url,
            'issuee': issuee,
        }

    def __unicode__(self):
        return "%s accepted %s from %s" % (self.issue.user, self.issue.badge, self.issue.issuer )

