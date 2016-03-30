from django.conf.urls import patterns, url

from Provisioning import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^index$', views.index, name='index'),
    url(r'^export', views.export, name='export'),
    # config/SN0123456789/MAC0123456789ABCDEF/PNSPA503/HW2.6.3/SW2.2.1
    # config/$SN/$MAU/$PN/$HWVER/$SWVER
    url(r'^config/(?P<sn>[\w|\W]+)/(?P<mac>[\w|\W]+)/(?P<pdn>[\w|\W]+)/(?P<hwv>[\w|\W]+)/(?P<swv>[\w|\W]+)$', views.config),
	# configOK/$SN/$MAU/$PN/$HWVER/$SWVER
    url(r'^configOK/(?P<sn>[\w|\W]+)/(?P<mac>[\w|\W]+)/(?P<pdn>[\w|\W]+)/(?P<hwv>[\w|\W]+)/(?P<swv>[\w|\W]+)$', views.configok),
    # firmware/$SN/$MAU/$PN/$HWVER/$SWVER
    url(r'^firmware/(?P<sn>[\w|\W]+)/(?P<mac>[\w|\W]+)/(?P<pdn>[\w|\W]+)/(?P<hwv>[\w|\W]+)/(?P<swv>[\w|\W]+)$', views.firmware),
)
