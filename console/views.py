from console.models import Power

from django.http import HttpResponseRedirect
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.encoding import smart_unicode
import logging


logger = logging.getLogger(__name__)
BATCH_SIZE = 48

# Create your views here.

def index(request, params={}):
    q = parse_param(request, 'query')
    rparams = dict(params)
    rparams['page'] = parse_param(request, 'page')
    rparams['query'] = q
    rparams['sender'] = 'index'
    results = search_powers(q, {'page': rparams['page']})
    rparams['results'] = results
    logger.debug("Got index request here... query=" + q)
    return render_to_response('index.html', rparams,
                              context_instance=RequestContext(request))


def search_powers(q, params):
    res = {}
    fltr = Power.objects.order_by('-updated_at')
    # if q:
    #    fltr = fltr.filter(identifier__startswith=q)

    paginator = Paginator(fltr, BATCH_SIZE)
    res['count'] = fltr.count()
    try:
        res['powers'] = paginator.page(params['page'])
    except PageNotAnInteger:
        res['powers'] = paginator.page(1)
    except EmptyPage:
        res['powers'] = paginator.page(paginator.num_pages)
    return res

def signout(request):
    logout(request)
    params = {}
    params['alert'] = "Signed out..."
    return index(request, params)


def signin(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    params = {}
    if user:
        if user.is_active:
            login(request, user)
            params['info'] = "You are logged in!"
        else:
            params['alert'] = "Failed signing in!"
    else:
        params['alert'] = "Failed signing in!"

    return index(request, params)

def parse_param(request, name):
    q = ''
    if name in request.POST:
        q = smart_unicode(request.POST.get(name))
    if name in request.GET:
        q = smart_unicode(request.GET.get(name))
    return q
