from console.models import Power
from console.forms import PowerForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django.utils.encoding import smart_unicode
import logging


logger = logging.getLogger(__name__)
BATCH_SIZE = 48


# Create your views here.
@login_required(login_url='/accounts/login/')
def index(request, params={}):
    rparams = dict(params)
    rparams['page'] = parse_param(request, 'page')
    rparams['sender'] = 'index'
    results = search_powers(None, {'page': rparams['page']})
    rparams['results'] = results
    rparams['form'] = PowerForm()
    return render_to_response('index.html', rparams,
                              context_instance=RequestContext(request))


@login_required(login_url='/accounts/login/')
def edit(request, power_id, params={}):
    if request.method == 'POST':
        power = Power.objects.get(pk=power_id)
        form = PowerForm(request.POST, instance=power)
        if form.is_valid():  # All validation rules pass
            prev = Power.objects.filter(id__lt=form.instance.id).order_by('-created_at')[0]
            form.save()
            _calculate(prev, form.instance)
            return HttpResponseRedirect("/")
    else:
        if power_id:
            power = Power.objects.get(pk=power_id)
            form = PowerForm(instance=power)
            form.id = power_id
        else:
            form = PowerForm()

    return render(request, 'register.html', {
        'sender': 'edit',
        'form': form,
        'power_id': power_id
    })


@login_required(login_url='/accounts/login/')
def delete(request, power_id, params={}):
    if request.method == 'POST':
        power = Power.objects.get(pk=power_id)
        power.delete()
        print "Deleted %s " % power_id
    return HttpResponseRedirect("/")


@login_required(login_url='/accounts/login/')
def register(request, params={}):
    if request.method == 'POST':
        form = PowerForm(request.POST)
        if form.is_valid():  # All validation rules pass
            prev = Power.objects.order_by('-created_at')[0]
            form.save()
            _calculate(prev, form.instance)
            return HttpResponseRedirect("/")
    return index(request, params)


@login_required(login_url='/accounts/login/')
def recalculate(request, params={}):
    prev = None
    for p in Power.objects.order_by('created_at'):
        _calculate(prev, p)
        prev = p
    return index(request, params)


def _calculate(prev, current):
    if prev and current and current.level >= prev.level:
        consume = current.level - prev.level
        duration = current.created_at - prev.created_at
        mins = duration.seconds % 3600 / 60
        hours = (duration.seconds / 3600)
        days = duration.days
        if days:
            hours += (days * 24)
        if mins > 30:
            hours += 1
        if hours:
            mins += (hours * 60)
        if not hours:
            hours = 1

        print("Hours between: %s" % hours)
        consume_per_hour = (consume + 0.0) / hours
        current.hourly_consume = consume_per_hour
        current.save()
        print("Calculated consume per hour: %s" % (consume_per_hour))
    

def search_powers(q, params):
    res = {}
    fltr = Power.objects.order_by('-created_at')
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
