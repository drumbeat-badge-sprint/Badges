from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from badges.models import Badge, BadgeClaim, BadgeIssue, Offering, Issuer,\
    BadgeRequest
from openid_provider.models import OpenID
from django.core.urlresolvers import reverse, resolve
from badges.forms import BadgeRequestForm
from django.contrib import messages
import badges
import urls
from urlparse import urlparse

try:
    import json
except ImportError:
    import simplejson as json

def badge(request, badge_id):
    badge = get_object_or_404(Badge, id=badge_id)
    return render_to_response('badges/badge.html', {
        'badge': badge,
    }, context_instance=RequestContext(request))

def badges(request):
    badges = Badge.objects.all()
    return render_to_response('badges/badges.html', {
        'badges': badges,
    }, context_instance=RequestContext(request))

@login_required
def index(request):
    return render_to_response('badges/index.html', {
        'issues': BadgeIssue.objects.filter(user=request.user,accepted=False),
        'claimed': BadgeClaim.objects.filter(issue__user=request.user),
    }, context_instance=RequestContext(request))
    
def issuer(request, issuer_id):
    issuer = get_object_or_404(Issuer, id=issuer_id)
    
    return render_to_response('badges/issuer.html', {
        'issuer': issuer,
    }, context_instance=RequestContext(request))

@login_required
def issue(request):
    if request.method == "GET":
        return HttpResponseRedirect(reverse("badges_index"))
    
    if request.POST['request_id'] != None:
        badge_request = BadgeRequest.objects.get(id=int(request.POST['request_id']))
    else:
        badge_request = None
        
    issuers = Issuer.objects.filter(users=request.user,id=badge_request.issuer_id)
    
    if issuers.count() > 0:    
        if request is not None:
            badge = badge_request.badge
            recipient = badge_request.user
        else: 
            badge = Badge.objects.get(id=int(request.POST['badge_id']))
            recipient = User.objects.get(id=int(request.POST['user_id']))
        issuer = issuers[0]
        issue,created = BadgeIssue.objects.get_or_create(badge=badge,user=recipient,issuer=issuer,request=badge_request)
        
        if created:
            messages.add_message(request, messages.INFO, 'You have issued %s to %s.' % (badge_request.badge,badge_request.user))
        else:
            messages.add_message(request, messages.ERROR, 'You have already issued %s to %s.' % (badge_request.badge,badge_request.user))
            
    
    return HttpResponseRedirect(reverse("badges_requests"))
            
def issues(request, username):
    user = get_object_or_404(User, username=username)
    issues = BadgeIssue.objects.filter(user=user,accepted=False)
    issued_badges = []
    for issue in issues:
        issued_badges.append(issue.serialized())
    return HttpResponse(json.dumps(issued_badges), mimetype='application/json')

@login_required
def claim(request):
    if request.method == "GET":
        return HttpResponseRedirect(reverse("badges_index"))
    issue = get_object_or_404(BadgeIssue,id=int(request.POST['issue_id']),user=request.user)
    
    claim = BadgeClaim.objects.create(issue=issue)
    issue.accepted = True
    issue.save()
    return HttpResponseRedirect(reverse("badges_index"))

@login_required
def claim_json(request):
    if request.method == "GET":
        return HttpResponseRedirect(reverse("badges_index"))

    print request.POST
    
    badge_view = resolve(urlparse(request.POST["badgeURL"])[2])
    badge_id = int(badge_view.kwargs['badge_id'])

    issuer_view = resolve(urlparse(request.POST["issuer"])[2])
    issuer_id = int(issuer_view.kwargs['issuer_id']) 
    
    issue = get_object_or_404(BadgeIssue,badge__id=badge_id,issuer__id=issuer_id,user=request.user)
    
    claim,created = BadgeClaim.objects.get_or_create(issue=issue)
    issue.accepted = True
    issue.save()
    return HttpResponse(json.dumps([claim.serialized()]), mimetype='application/json')

def claims(request, username):
    user = get_object_or_404(User, username=username)
    claims = BadgeClaim.objects.filter(issue__user=user)
    badges = []
    for claim in claims:
        badges.append(claim.serialized())
    return HttpResponse(json.dumps(badges), mimetype='application/json')
            

@login_required
def drop(request):
    if request.method == "GET":
        return HttpResponseRedirect(reverse("badges_index"))
    claim = BadgeClaim.objects.get(id=int(request.POST['claim_id']))
    claim.delete()
    return HttpResponseRedirect(reverse("badges_index"))

@login_required
def request(request,issuer_id=None,badge_id=None):
    if request.method == "GET":
        issuer = get_object_or_404(Issuer, pk=issuer_id)
        badge = get_object_or_404(Badge, pk=badge_id)
        #request = BadgeRequest(issuer=issuer,badge=badge,user=request.user)
        form = BadgeRequestForm(initial={"issuer":issuer,"badge":badge})

        return render_to_response('badges/request.html', {
            'issuer': issuer,
            'badge': badge,
            'form': form,
        }, context_instance=RequestContext(request))


    form = BadgeRequestForm(request.POST)
    
    if not form.is_valid():
        return HttpResponseRedirect(reverse("badges_index"))
    
    badge_request = form.save(commit=False)
    badge_request.user = request.user
    form.save()
    messages.add_message(request, messages.INFO, 'You have requested %s from %s.' % (badge_request.badge,badge_request.issuer))
    
    return HttpResponseRedirect(reverse("badges_badges"))

@login_required
def request_json(request):
    if request.method == "GET":
        return HttpResponseRedirect(reverse("badges_index"))

    badge_view = resolve(urlparse(request.POST["badgeURL"])[2])
    badge_id = int(badge_view.kwargs['badge_id'])
    badge = get_object_or_404(Badge,id=badge_id)
    
    issuer_view = resolve(urlparse(request.POST["issuer"])[2])
    issuer_id = int(issuer_view.kwargs['issuer_id']) 
    issuer = get_object_or_404(Issuer,id=issuer_id)
    
    evidence = request.POST.get("evidence","")
    evidenceURL = request.POST.get("evidenceURL",None)
    
    badge_request, created = BadgeRequest.objects.get_or_create(badge=badge,issuer=issuer,user=request.user)
    
    badge_request.evidence=evidence
    badge_request.evidenceURL=evidenceURL
    badge_request.save()
    
    return HttpResponse(json.dumps([badge_request.serialized()]), mimetype='application/json')


@login_required
def requests(request):
    issuers = Issuer.objects.filter(users=request.user)
    
    return render_to_response('badges/requests.html', {
        'issuers': issuers,
    }, context_instance=RequestContext(request))

    #messages.add_message(request, messages.INFO, 'You have issued %s from %s.' % (badge_request.badge,badge_request.issuer))
    
    return HttpResponseRedirect(reverse("badges_index"))

