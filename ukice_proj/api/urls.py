from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'accidents_in_rect/?$', 'ukice_proj.api.views.accidents_in_rect'),
    url(r'freezetweets_national/?$', 'ukice_proj.api.views.freezetweets_national'),
    url(r'freezetweets_near/?$', 'ukice_proj.api.views.freezetweets_near'),
    # Examples:
    # url(r'^$', 'ukice_proj.views.home', name='home'),
    # url(r'^ukice_proj/', include('ukice_proj.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
