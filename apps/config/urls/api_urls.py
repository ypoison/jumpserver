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
    path('node-config/reload/', api.NodeReloadApi.as_view(), name='node-config-reload'),
    path('web-config/get-info/<uuid:pk>/', api.GetApi.as_view(), name='web-config-get'),

]

urlpatterns += router.urls