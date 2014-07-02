from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # Change index to home when everything is ready
    url(r'^$', 'openshift.views.index', name='home'),
    url(r'^select-person/?$', 'openshift.views.select_person', name='select_person'),
    url(r'^map/?$', 'openshift.views.map', name='map'),
    url(r'^timeline/?$', 'openshift.views.timeline', name='timeline'),
    url(r'^test$', 'openshift.views.test', name='test'),
    url(r'^test3$', 'openshift.views.test3', name='test3'),
    # url(r'^openshift/', include('openshift.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

handler404 = 'openshift.views.custom_404'
handler500 = 'openshift.views.custom_500'
