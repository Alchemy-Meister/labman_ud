from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings

from dajaxice.core import dajaxice_autodiscover, dajaxice_config
dajaxice_autodiscover()

import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'projects_morelab.views.home', name = 'home'),
    url(r'^login/$', 'django.contrib.auth.views.login'),
    url(r'^logout/$', 'projects_morelab.views.logout_view', name = 'logout_view'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^organizations/', include('organization_manager.urls')),
    url(r'^employees/', include('employee_manager.urls')),
    url(r'^projects/', include('project_manager.urls')),
    url(r'^funding_calls/', include('funding_call_manager.urls')),

    # Just for development purposes, serve in another way in production
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),

    url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
)

urlpatterns += staticfiles_urlpatterns()
