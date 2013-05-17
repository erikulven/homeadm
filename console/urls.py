from django.conf.urls import patterns, url


urlpatterns = patterns('',
    url(r'^$', 'views.index'),
    url(r'^index/', 'views.index'),
    url(r'^signin/$', 'console.signin'),
    url(r'^signout/$', 'console.signout'),
)
