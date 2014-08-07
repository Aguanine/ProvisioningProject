from django.conf.urls import patterns, url

from Provisioning import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^index$', views.index, name='index'),
    # config/SN0123456789/MAC0123456789ABCDEF/PNSPA503/SW2.2.1
    url(r'^config/(?P<sn>[\w|\W]+)/(?P<mac>[\w|\W]+)/(?P<pdn>[\w|\W]+)/(?P<swv>[\w|\W]+)$', views.config),
    url(r'^firmware/(?P<sn>[\w|\W]+)/(?P<mac>[\w|\W]+)/(?P<pdn>[\w|\W]+)/(?P<swv>[\w|\W]+)$', views.firmware),
)
