from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', include('Provisioning.urls')),
    # url(r'^blog/', include('blog.urls')),
    url(r'^provisioning/', include('Provisioning.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
