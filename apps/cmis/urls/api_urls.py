# ~*~ coding: utf-8 ~*~
from __future__ import unicode_literals
from django.urls import path
from rest_framework.routers import DefaultRouter
from .. import api

app_name = 'cmis'

router = DefaultRouter()

router.register(r'account', api.AccountViewSet, 'account')
router.register(r'cdn', api.CDNDomainViewSet, 'cdn')

urlpatterns = [
    path('chost/get-info/', api.CloudInfoAPI.as_view(), name='chost-get-info'),
    path('chost/create/record/', api.ChostCreateRecordAPI.as_view(), name='chost-create-record'),
    path('chost/get-price/', api.GetPriceAPI.as_view(), name='chost-get-price'),
    path('chost/set-model/', api.SetModelAPI.as_view(), name='chost-set-model'),
    path('chost/<uuid:pk>/get-status/', api.GetStatusAPI.as_view(), name='chost-get-status'),
    path('chost/for-model/<pk>/', api.ForModelAPI.as_view(), name='chost-for-model'),

    path('cdn/<uuid:pk>/modify/', api.CDNDomainModifyApi.as_view(), name='cdn-modify'),
    path('cdn/<uuid:pk>/update/', api.CDNDomainUpdateApi.as_view(), name='cdn-update'),
    path('cdn/full/update/', api.CDNDomainUpdateApi.as_view(), name='cdn-update'),
    path('cdn/<uuid:pk>/set/', api.CDNDomainSetApi.as_view(), name='cdn-set'),
    path('cdn/<uuid:pk>/oss/get/', api.OSSGetApi.as_view(), name='oss-get'),
    path('cdn/fresh/', api.CDNFreshSetApi.as_view(), name='cdn-fresh-list'),
    path('cdn/fresh/<uuid:pk>/remain/get/', api.CDNFreshGetRemainApi.as_view(), name='cdn-fresh-remain-get'),
]

urlpatterns += router.urls