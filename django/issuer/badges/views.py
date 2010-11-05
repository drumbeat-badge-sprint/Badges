from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from badges.models import Badge, BadgeClaim
from openid_provider.models import OpenID

try:
    import json
except ImportError:
    import simplejson as json

@login_required
def index(request):
    return render_to_response('badges/index.html', {
        'badges': Badge.objects.all(),
        'claimed': BadgeClaim.objects.filter(user=request.user),
    }, context_instance=RequestContext(request))

@login_required
def claim(request):
    if request.method == "GET":
        return HttpResponseRedirect('/badges/')
    badge = Badge.objects.get(id=int(request.POST['badge_id']))
    claim = BadgeClaim(
        user=request.user,
        badge=badge
    )
    claim.save()
    return HttpResponseRedirect('/badges/')

def drop(request):
    if request.method == "GET":
        return HttpResponseRedirect('/badges/')
    claim = BadgeClaim.objects.get(id=int(request.POST['claim_id']))
    claim.delete()
    return HttpResponseRedirect('/badges/')

def badge(request, badge_id):
    badge = get_object_or_404(Badge, id=badge_id)
    return HttpResponse(badge.title)

def badges(request, username):
    user = get_object_or_404(User, username=username)
    claims = BadgeClaim.objects.filter(user=user)
    badges = []
    for claim in claims:
        badges.append(claim.serialized())
    return HttpResponse(json.dumps(badges), mimetype='application/json')
            
