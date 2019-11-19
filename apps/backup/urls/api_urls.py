# ~*~ coding: utf-8 ~*~
from __future__ import unicode_literals
from django.urls import path
from rest_framework.routers import DefaultRouter
from .. import api

app_name = 'backup'

router = DefaultRouter()

router.register(r'records', api.RecordsViewSet, 'record')

urlpatterns = [
    path('records/update/', api.RecordsUpdateApi.as_view(), name='records-update'),
    path('records/platform/tree/', api.RecordsPlatformAsTreeApi.as_view(), name='records-platform-tree'),
]

urlpatterns += router.urls