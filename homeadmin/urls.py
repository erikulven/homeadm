from django.conf.urls import patterns, include, url
from django.contrib import admin
import settings


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'console.views.index', name='index'),
    url(r'^console/', 'console.views.index'),
    url(r'^index/', 'console.views.index'),
    url(r'^register/$', 'console.views.register'),
    url(r'^recalculate/$', 'console.views.recalculate'),
    url(r'^edit/(?P<power_id>.*)/$', 'console.views.edit'),
    url(r'^delete/(?P<power_id>.*)/$', 'console.views.delete'),
    url(r'^signin/$', 'console.views.signin'),
    url(r'^signout/$', 'console.views.signout'),
    url(r'^admin/', include(admin.site.urls)),
    (r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'registration/login.html'}),
)


if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    )
