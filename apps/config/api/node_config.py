# ~*~ coding: utf-8 ~*~

from rest_framework_bulk import BulkModelViewSet
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.generics import (
    ListAPIView,
)
from common.utils import get_logger, get_object_or_none
from common.permissions import IsOrgAdmin

from assets.models import Node
from ..models import WEBConfigRecords
from .. import serializers

logger = get_logger(__file__)
__all__ = ['NodeViewSet','WEBConfigViewSet','GetPrivateApi',
           'GetProxyIPApi',
           ]

class NodeViewSet(BulkModelViewSet):
    filter_fields = ("value", "public_node_asset", "private_node_asset")
    search_fields = filter_fields
    permission_classes = (IsOrgAdmin,)
    serializer_class = serializers.NodeConfigSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        self.queryset = Node.objects.filter(key__regex=r'^1:[0-9]$').exclude(code="GGDLJD").exclude(public_node_asset__isnull=True)
        return self.queryset

class WEBConfigViewSet(BulkModelViewSet):
    filter_fields = ('domain', 'port', 'proxy_ip', 'proxy_port', 'comment')
    search_fields = filter_fields
    queryset = WEBConfigRecords.objects.all()
    permission_classes = (IsOrgAdmin,)
    serializer_class = serializers.WEBConfigSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        queryset = super().get_queryset().all()
        print(queryset)
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

class GetProxyIPApi(ListAPIView):
    permission_classes = (IsOrgAdmin,)
    serializer_class = serializers.PrivateAssetSerializer

    def get_queryset(self):
        node_id = self.kwargs.get('pk', '')
        queryset = []

        if not node_id:
            return queryset
        try:
            queryset = []
            asset = Node.objects.get(id=node_id).private_node_asset
            if asset.ip:
                queryset.append({'hostname':asset.hostname,'ip':asset.ip})
            if asset.public_ip:
                queryset.append({'hostname':asset.hostname,'ip':asset.public_ip})
        except:
            queryset = []
        return queryset