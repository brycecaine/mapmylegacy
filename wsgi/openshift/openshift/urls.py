from django.conf.urls import patterns, include, url
from mapmylegacy import views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # Change index to home when everything is ready
    url(r'^$', views.home, name='home'),
    url(r'^select-person/?$', views.select_person, name='select_person'),
    url(r'^map/?$', views.map, name='map'),
    url(r'^timeline/?$', views.timeline, name='timeline'),
    url(r'^logout/?$', views.logout, name='logout'),
    # url(r'^openshift/', include('openshift.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

handler404 = views.custom_404
handler500 = views.custom_500
