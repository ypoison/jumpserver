# ~*~ coding: utf-8 ~*~

from rest_framework_bulk import BulkModelViewSet
from rest_framework.views import APIView, Response
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import generics

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

class GetPrivateApi(generics.RetrieveAPIView):
    queryset = Node.objects.all()
    permission_classes = (IsOrgAdmin,)
    serializer_class = serializers.PrivateAssetSerializer
    def retrieve(self, request, *args, **kwargs):
        node_id = kwargs.get('pk')
        private_asset = Node.objects.get(id=node_id).get_children().get(value='other').get_all_assets().list()
        print(private_asset)
        serializer = serializers.PrivateAssetSerializer(instance=private_asset)
        return Response(serializer.data)