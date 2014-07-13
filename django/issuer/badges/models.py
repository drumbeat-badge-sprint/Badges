from django.contrib.auth.models import User
from django.contrib import admin
from django.db import models

from openid_provider.models import OpenID
import settings
import calendar
import datetime
from django.core.urlresolvers import reverse

try:
    import json
except ImportError:
    import simplejson as json
    
class Issuer(models.Model):
    users = models.ManyToManyField(User,related_name="issuers")
    name = models.CharField(max_length=125)
    url = models.URLField()
    timestamp = models.DateTimeField(auto_now_add=True)
    issuable_badges = models.ManyToManyField("Badge",related_name="issuers",through="Offering",blank=True)

    def get_absolute_url(self):
        return reverse("badges_issuer", args=[self.pk])
    
    def __unicode__(self):
        return self.name

class Badge(models.Model):
    title = models.CharField(max_length=125)
    description = models.TextField()
    image = models.ImageField(upload_to="badges/",null=True,blank=True)
    imageURL = models.URLField(null=True,blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse("badges_badge", args=[self.pk])
    
    def __unicode__(self):
        return self.title
    
class Offering(models.Model):
    badge = models.ForeignKey(Badge,related_name="offerings")
    issuer = models.ForeignKey(Issuer,related_name="offerings")
    timestamp = models.DateTimeField(auto_now_add=True)
    requirements = models.TextField(blank=True)
    requirementsURL = models.URLField(blank=True,null=True)

    def __unicode__(self):
        return "%s offers %s" % (self.issuer, self.badge)
    
class BadgeRequestManager(models.Manager):
    
    def open(self):
        return self.filter(issue__isnull=True)

class BadgeRequest(models.Model):
    """
    BadgeIssue represents an attempt by an Issuer to grant a user a badge.  
    If the user accepts, the BadgeIssue is marked as accepted and a BadgeClaim is created.
    """
    user = models.ForeignKey(User,related_name="requests")
    badge = models.ForeignKey(Badge,related_name="requests")
    timestamp = models.DateTimeField(auto_now_add=True)
    expires = models.DateTimeField(default=datetime.datetime(year=2100,month=12,day=31))
    issuer = models.ForeignKey(Issuer,related_name="requests")
    evidence = models.TextField(blank=True)
    evidenceURL = models.URLField(blank=True,null=True)
    
    objects = BadgeRequestManager()

    def create_issue(self):
        return BadgeIssue.objects.create(user=self.user,
                                         badge=self.badge,
                                         request=self,
                                         issuer=self.issuer)

    def json(self):
        return json.dumps(self.serialized())

    def serialized(self):
        issuee = [
                {
                    'type': 'email',
                    'id': self.user.email
                }
                ]
        
        try:
            openid = OpenID.objects.get(user=self.user)
            issuee.append({
                                'type': 'openid',
                                'id': settings.HOST_SERVER + '/openid/%s/' % (openid.openid,),
                            })
                
        except OpenID.DoesNotExist:
            openid = None
            
        
        if self.badge.image.name is not None:
            image_url = settings.HOST_SERVER + self.badge.image.url
        else:
            image_url = self.badge.imageURL
            
        return {
            'id': self.badge.pk,
            'schema': 'http://example.org/badge/%d' % (self.badge.pk,),
            'mustSupport': [],
            'title': self.badge.title,
            'description': self.badge.description,
            'timestamp': calendar.timegm(self.timestamp.timetuple()),
            'expires': calendar.timegm(self.expires.timetuple()),
            'badgeURL': settings.HOST_SERVER + self.badge.get_absolute_url(),
            'issuer': settings.HOST_SERVER + self.issuer.get_absolute_url(),
            'issuerURL': self.issuer.url,
            'issuerName': self.issuer.name,
            'imageURL': image_url,
            'issuee': issuee,
            'evidence': self.evidence,
            'evidenceURL': self.evidenceURL,
        }
        
    def __unicode__(self):
        return "%s requested %s from %s" % (self.user, self.badge, self.issuer )

class BadgeIssue(models.Model):
    """
    BadgeIssue represents an attempt by an Issuer to grant a user a badge.  
    If the user accepts, the BadgeIssue is marked as accepted and a BadgeClaim is created.
    """
    user = models.ForeignKey(User,related_name="issues")
    badge = models.ForeignKey(Badge,related_name="issues")
    request = models.OneToOneField(BadgeRequest,related_name="issue",null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    expires = models.DateTimeField(default=datetime.datetime(year=2100,month=12,day=31))
    issuer = models.ForeignKey(Issuer,related_name="issues")
    accepted = models.BooleanField(default=False)

    def json(self):
        return json.dumps(self.serialized())

    def serialized(self):
        issuee = [
                {
                    'type': 'email',
                    'id': self.user.email
                }
                ]
        
        try:
            openid = OpenID.objects.get(user=self.user)
            issuee.append({
                                'type': 'openid',
                                'id': settings.HOST_SERVER + '/openid/%s/' % (openid.openid,),
                            })
                
        except OpenID.DoesNotExist:
            openid = None
            
        
        if self.badge.image.name is not None:
            image_url = settings.HOST_SERVER + self.badge.image.url
        else:
            image_url = self.badge.imageURL
            
        return {
            'id': self.badge.pk,
            'schema': 'http://example.org/badge/%d' % (self.badge.pk,),
            'mustSupport': [],
            'title': self.badge.title,
            'description': self.badge.description,
            'timestamp': calendar.timegm(self.timestamp.timetuple()),
            'expires': calendar.timegm(self.expires.timetuple()),
            'badgeURL': settings.HOST_SERVER + self.badge.get_absolute_url(),
            'issuer': settings.HOST_SERVER + self.issuer.get_absolute_url(),
            'issuerURL': self.issuer.url,
            'issuerName': self.issuer.name,
            'imageURL': image_url,
            'issuee': issuee,
            'accepted': self.accepted,
        }
        
    def __unicode__(self):
        return "%s issued %s to %s" % (self.issuer, self.badge, self.user)



class BadgeClaim(models.Model):
    issue = models.ForeignKey(BadgeIssue,related_name="claims")
    timestamp = models.DateTimeField(auto_now_add=True)

    def json(self):
        return json.dumps(self.serialized())

    def serialized(self):
        result = self.issue.serialized()
        result["timestamp"] = calendar.timegm(self.timestamp.timetuple())
        return result

    def __unicode__(self):
        return "%s accepted %s from %s" % (self.issue.user, self.issue.badge, self.issue.issuer )

