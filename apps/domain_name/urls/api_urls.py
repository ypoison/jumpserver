# ~*~ coding: utf-8 ~*~
from __future__ import unicode_literals
from django.urls import path
from rest_framework.routers import DefaultRouter
from .. import api

app_name = 'domain-name'

router = DefaultRouter()

router.register(r'domain-name', api.DomainNameViewSet, 'domain-name')
router.register(r'domain-name-records', api.RecordsViewSet, 'records')
router.register(r'account', api.AccountViewSet, 'account')

urlpatterns = [
    path('domain-name/netapi-update/',api.DomainNameNetAPIUpdateApi.as_view(), name='domain-name-netapi-update'),
    path('domain-name/beian-check/<uuid:pk>/',api.DomainNameBeiAnCheckApi.as_view(), name='beian-check'),
    path('domain-name/gfw-check/<uuid:pk>/',api.DomainNameGFWCheckApi.as_view(), name='gfw-check'),
    path('domain-name/record/<uuid:pk>/',api.DomainNameRecordUpdateApi.as_view(), name='record-update-status'),

    path('domain-name-records/netapi-update/<uuid:pk>/',api.RecordsNetAPIUpdateApi.as_view(), name='records-netapi-update'),
]

urlpatterns += router.urls