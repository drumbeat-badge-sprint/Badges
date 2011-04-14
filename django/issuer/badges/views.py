from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from badges.models import Badge, BadgeClaim, BadgeIssue
from openid_provider.models import OpenID
from django.core.urlresolvers import reverse

try:
    import json
except ImportError:
    import simplejson as json

@login_required
def index(request):
    return render_to_response('badges/index.html', {
        'issues': BadgeIssue.objects.filter(user=request.user,accepted=False),
        'claimed': BadgeClaim.objects.filter(issue__user=request.user),
    }, context_instance=RequestContext(request))

@login_required
def issue(request):
    if request.method == "GET":
        return HttpResponseRedirect(reverse("badges_index"))
    badge = Badge.objects.get(id=request.POST['badge_id'])
    recipient = User.objects.get(id=request.POST['user_id'])
    issue = BadgeIssue(badge=badge,user=recipient,issuer=request.POST['issuer'])
    
    return HttpResponseRedirect(reverse("badges_index"))

@login_required
def claim(request):
    if request.method == "GET":
        return HttpResponseRedirect(reverse("badges_index"))
    issue = get_object_or_404(BadgeIssue,id=int(request.POST['issue_id']),user=request.user)
    
    claim = BadgeClaim.objects.create(issue=issue)
    issue.accepted = True
    issue.save()
    return HttpResponseRedirect(reverse("badges_index"))

def drop(request):
    if request.method == "GET":
        return HttpResponseRedirect(reverse("badges_index"))
    claim = BadgeClaim.objects.get(id=int(request.POST['claim_id']))
    claim.delete()
    return HttpResponseRedirect(reverse("badges_index"))

def badge(request, badge_id):
    badge = get_object_or_404(Badge, id=badge_id)
    return HttpResponse(badge.title)

def badges(request, username):
    user = get_object_or_404(User, username=username)
    claims = BadgeClaim.objects.filter(issue__user=user)
    badges = []
    for claim in claims:
        badges.append(claim.serialized())
    return HttpResponse(json.dumps(badges), mimetype='application/json')
            
