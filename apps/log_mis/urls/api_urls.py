# ~*~ coding: utf-8 ~*~
from __future__ import unicode_literals
from django.urls import path
from rest_framework.routers import DefaultRouter
from .. import api

app_name = 'log-mis'

router = DefaultRouter()

router.register(r'records', api.RecordsViewSet, 'record')

urlpatterns = [
    path('records/update/', api.RecordsUpdateApi.as_view(), name='records-update'),
    path('records/platform/tree/', api.RecordsPlatformAsTreeApi.as_view(), name='records-platform-tree'),
    path('records/share/<uuid:pk>/', api.ShareApi.as_view(), name='log-share'),
    path('records/<uuid:pk>/refresh/', api.RefreshNodeRecordInfoApi.as_view(), name='node-refresh-record-info'),
]

urlpatterns += router.urls