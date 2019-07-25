# ~*~ coding: utf-8 ~*~
from __future__ import unicode_literals
from django.urls import path
from rest_framework.routers import DefaultRouter
from .. import api

app_name = 'cmis'

router = DefaultRouter()

router.register(r'account', api.AccountViewSet, 'account')

urlpatterns = [
    path('cmis-chost/get-info/', api.CloudInfoAPI.as_view(), name='chost-get-info'),
]

urlpatterns += router.urls