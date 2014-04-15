from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'openshift.views.home', name='home'),
    url(r'^select-person/?$', 'openshift.views.home', name='home'),
    url(r'^map/?$', 'openshift.views.map', name='map'),
    url(r'^timeline/?$', 'openshift.views.timeline', name='timeline'),
    url(r'^logout/?$', 'openshift.views.logout', name='logout'),
    # url(r'^openshift/', include('openshift.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

handler404 = 'openshift.views.custom_404'
handler500 = 'openshift.views.custom_500'
