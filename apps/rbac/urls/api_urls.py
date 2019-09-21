# ~*~ coding: utf-8 ~*~
from __future__ import unicode_literals
from django.urls import path
from rest_framework.routers import DefaultRouter
from .. import api

app_name = 'rbac'

router = DefaultRouter()

router.register(r'menu', api.MenuViewSet, 'menu')

urlpatterns = [
    path('menu/perms/', api.MenuPermsAPI.as_view(), name='menu-perms'),
    path('perms/<uuid:pk>/edit/', api.PermsEditAPI.as_view(), name='perms-edit'),
]

urlpatterns += router.urls