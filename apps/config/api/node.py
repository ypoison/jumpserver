# ~*~ coding: utf-8 ~*~

from rest_framework_bulk import BulkModelViewSet
from rest_framework.views import APIView, Response
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import generics

from common.utils import get_logger, get_object_or_none
from common.permissions import IsOrgAdmin

from ..models import PlatformNode
from .. import serializers

logger = get_logger(__file__)
__all__ = ['NodeViewSet',
           ]

class NodeViewSet(BulkModelViewSet):
    filter_fields = ("platform", "public_node", "private_node")
    search_fields = filter_fields
    queryset = PlatformNode.objects.all()
    permission_classes = (IsOrgAdmin,)
    serializer_class = serializers.NodeSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        queryset = super().get_queryset().all()
        return queryset