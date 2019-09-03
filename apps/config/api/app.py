# ~*~ coding: utf-8 ~*~

from rest_framework_bulk import BulkModelViewSet
from rest_framework.pagination import LimitOffsetPagination

from common.utils import get_logger
from common.permissions import IsValidUser

from ..models import App
from .. import serializers

logger = get_logger(__file__)
__all__ = ['AppViewSet',
           ]

class AppViewSet(BulkModelViewSet):
    filter_fields = ('name', 'type', 'port')
    search_fields = filter_fields
    queryset = App.objects.all()
    permission_classes = (IsValidUser,)
    serializer_class = serializers.AppSerializer
    pagination_class = LimitOffsetPagination