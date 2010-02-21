from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from django.views.generic.simple import direct_to_template

urlpatterns = patterns('',
    (r'^', direct_to_template, {
        'template': 'main.html'
    }),

    (r'^admin/', include(admin.site.urls)),
)
