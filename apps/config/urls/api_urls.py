# ~*~ coding: utf-8 ~*~
from __future__ import unicode_literals
from django.urls import path
from rest_framework.routers import DefaultRouter
from .. import api

app_name = 'config'

router = DefaultRouter()

router.register(r'high-anti', api.NodeViewSet, 'high-anti')

urlpatterns = [

]

urlpatterns += router.urls