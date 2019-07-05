# ~*~ coding: utf-8 ~*~

from rest_framework_bulk import BulkModelViewSet
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.generics import (
    ListAPIView,
)
from common.utils import get_logger, get_object_or_none
from common.permissions import IsOrgAdmin

from assets.models import Node
from .. import serializers

logger = get_logger(__file__)
__all__ = ['NodeRecordsViewSet','GetPrivateApi'
           ]

class NodeRecordsViewSet(BulkModelViewSet):
    filter_fields = ("platfrom", "domain", "proxy_ip")
    search_fields = filter_fields
    queryset = Node.objects.all()
    permission_classes = (IsOrgAdmin,)
    serializer_class = serializers.NodeSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        queryset = super().get_queryset().all()
        return queryset

class GetPrivateApi(ListAPIView):
    permission_classes = (IsOrgAdmin,)
    serializer_class = serializers.PrivateAssetSerializer

    def get_queryset(self):
        node_id = self.kwargs.get('pk', '')
        queryset = []

        if not node_id:
            return queryset
        try:
            queryset = list(Node.objects.get(id=node_id).get_children().get(value='other').get_all_assets())
        except:
            queryset = []
        return queryset