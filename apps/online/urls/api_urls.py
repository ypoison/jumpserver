# ~*~ coding: utf-8 ~*~
from __future__ import unicode_literals
from django.urls import path
from rest_framework.routers import DefaultRouter
from .. import api

app_name = 'online'

router = DefaultRouter()

#router.register(r'records', api.RecordsViewSet, 'record')

urlpatterns = [
    path('number/update/', api.OnlineNumberUpdateApi.as_view(), name='online-update'),
    path('dashboard/update/', api.DashboardUpdateApi.as_view(), name='dashboard-update'),
]

#urlpatterns += router.urls