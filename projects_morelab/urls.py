from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'projects_morelab.views.home', name='home'),
    # url(r'^projects_morelab/', include('projects_morelab.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),

    (r'^organizaciones/', include('organization_manager.urls')),
    (r'^personas/', include('employee_manager.urls')),
    (r'^proyectos/', include('project_manager.urls')),
)
