# ~*~ coding: utf-8 ~*~

from rest_framework_bulk import BulkModelViewSet
from rest_framework.pagination import LimitOffsetPagination

from common.utils import get_logger, get_object_or_none
from common.permissions import IsOrgAdmin

from ..models import Account
from .. import serializers


logger = get_logger(__file__)
__all__ = ['AccountViewSet',]

class AccountViewSet(BulkModelViewSet):
    filter_fields = ("name", "cloud_service_providers")
    search_fields = filter_fields
    queryset = Account.objects.all()
    permission_classes = (IsOrgAdmin,)
    serializer_class = serializers.AccountSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        queryset = super().get_queryset().all()
        return queryset