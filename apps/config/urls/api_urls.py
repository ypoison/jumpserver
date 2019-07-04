# ~*~ coding: utf-8 ~*~
from __future__ import unicode_literals
from django.urls import path
from rest_framework.routers import DefaultRouter
from .. import api

app_name = 'config'

router = DefaultRouter()

router.register(r'node', api.NodeRecordsViewSet, 'records')

urlpatterns = [
    path('node-config/get-private/<uuid:pk>/', api.GetPrivateApi.as_view(), name='node-config-private-get'),

]

urlpatterns += router.urls