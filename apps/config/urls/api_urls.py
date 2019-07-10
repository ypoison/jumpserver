# ~*~ coding: utf-8 ~*~
from __future__ import unicode_literals
from django.urls import path
from rest_framework.routers import DefaultRouter
from .. import api

app_name = 'config'

router = DefaultRouter()

router.register(r'node-config', api.NodeViewSet, 'node-config')
router.register(r'web-config', api.WEBConfigViewSet, 'web-config')

urlpatterns = [
    path('node-config/get-private/<uuid:pk>/', api.GetPrivateApi.as_view(), name='node-config-private-get'),
    path('web-config/get-proxy-ip/<uuid:pk>/', api.GetProxyIPApi.as_view(), name='web-config-proxy-ip-get'),

]

urlpatterns += router.urls