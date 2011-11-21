from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^api/', include( 'api.urls' ) ),
	url(r'^$', 'ukice_proj.frontend.views.index'),
)
