# ~*~ coding: utf-8 ~*~
from __future__ import unicode_literals
from rest_framework.routers import DefaultRouter
from .. import api

app_name = 'cmis'

router = DefaultRouter()

router.register(r'account', api.AccountViewSet, 'account')

urlpatterns = router.urls