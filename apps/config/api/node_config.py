# ~*~ coding: utf-8 ~*~
from rest_framework.views import Response
from rest_framework_bulk import BulkModelViewSet
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.generics import (
    ListAPIView,
)
from common.utils import get_logger, get_object_or_none
from common.permissions import IsOrgAdmin

from assets.models import Node, Asset
from ..models import WEBConfigRecords
from .. import serializers
from ..webconfig import WEBConfig

logger = get_logger(__file__)
__all__ = ['NodeViewSet','NodeReloadApi', 'WEBConfigViewSet','GetApi',
           ]
webconfig = WEBConfig()

class NodeViewSet(BulkModelViewSet):
    filter_fields = ("platform", "node_asset")
    search_fields = ("platform__value", "node_asset__ip")
    permission_classes = (IsOrgAdmin,)
    serializer_class = serializers.NodeConfigSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        self.queryset = WEBConfigRecords.objects.values('platform','node_asset').distinct()
        return self.queryset

class NodeReloadApi(ListAPIView):
    permission_classes = (IsOrgAdmin,)
    serializer_class = serializers.PrivateAssetSerializer

    def post(self, request, *args, **kwargs):
        print(1111)
        action = self.request.POST.get('action')
        print(action)
        node_ip = self.request.POST.get('node')
        print(node_ip)
        return Response({"msg": "ok"})

class WEBConfigViewSet(BulkModelViewSet):
    filter_fields = ('domain', 'port', 'proxy_ip', 'proxy_port', 'comment')
    search_fields = filter_fields
    queryset = WEBConfigRecords.objects.all()
    permission_classes = (IsOrgAdmin,)
    serializer_class = serializers.WEBConfigSerializer
    pagination_class = LimitOffsetPagination

    def destroy(self, request, *args, **kwargs):
        web_config = self.get_object()
        kw= (web_config.__dict__)
        node_ip = web_config.node_asset.ip
        kw.update(node_ip=node_ip)
        platform = web_config.platform.code
        kw.update(platform=platform)
        del_web_config = webconfig.remove(**kw)
        if del_web_config['code']:
            web_config.delete()
            return Response({"msg": "ok"})
        else:
            return Response({'error': del_web_config['msg']}, status=400)

class GetApi(ListAPIView):
    permission_classes = (IsOrgAdmin,)
    serializer_class = serializers.PrivateAssetSerializer

    def get_queryset(self):
        action = self.request.GET.get('action')
        id = self.kwargs.get('pk', '')
        queryset = []
        if not id:
            return queryset
        if action == "getnode":
            queryset = list(Node.objects.get(code="GGDLJD").get_all_assets())
            asset =  list(Node.objects.get(id=id).get_children().get(value='other').get_all_assets())
            queryset.extend(asset)
        elif action == "getproxy":
            queryset =  list(Node.objects.get(id=id).get_all_assets())
        elif action == "getip":
            asset = get_object_or_none(Asset,id=id)
            queryset.append({'id':asset.ip,'ip':asset.ip,'hostname':asset.hostname})
            if asset.public_ip:
                queryset.append({'id':asset.ip,'ip':asset.public_ip,'hostname':asset.hostname})
        return queryset