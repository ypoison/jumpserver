# ~*~ coding: utf-8 ~*~
from rest_framework.views import Response
from rest_framework_bulk import BulkModelViewSet
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.generics import (
    ListAPIView,
)
from common.utils import get_request_ip, get_logger, get_object_or_none
from common.permissions import IsOrgAdmin

from assets.models import Node, Asset
from ..models import WEBConfigRecords
from .. import serializers
from ..webconfig import WEBConfig

from ..tasks import write_log_async

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
        action = self.request.data.get('action')
        node_asset_id = self.request.data.get('node')
        node_asset = get_object_or_none(Asset, id=node_asset_id)
        if node_asset:
            try:
                node_asset_ip = node_asset.ip
                kw = self.request.data
                kw['node'] = node_asset_ip
                if action == 'reload':
                    res = webconfig.reload(**kw)
                elif action == 'restart':
                    res = webconfig.restart(**kw)
                if res['code']:

                    login_ip = get_request_ip(self.request)
                    user_agent = self.request.user
                    data = {
                        'action': action,
                        'resource_type': '节点操作',
                        'remote_addr': login_ip,
                        'user': user_agent,
                        'resource':  str(node_asset)
                    }

                    write_log_async.delay(**data)
                    return Response({"msg": "ok"})
                else:
                    return Response({'error': res['msg']}, status=400)
            except Exception as e:
                Response({"error":  e}, status=400)
        else:
            return Response({"error": '获取节点主机信息失败'}, status=400)


class WEBConfigViewSet(BulkModelViewSet):
    filter_fields = ('platform__value', 'domain', 'port', 'proxy_ip', 'proxy_port', 'comment')
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
            asset = list(Node.objects.get(id=id).get_children().get(value='other').get_all_assets().filter(hostname__contains='Proxy'))
            queryset.extend(asset)
        elif action == "getproxy":
            queryset =  list(Node.objects.get(id=id).get_all_assets())
        elif action == "getip":
            asset = get_object_or_none(Asset,id=id)
            queryset.append({'id':asset.ip,'ip':asset.ip,'hostname':asset.hostname})
            if asset.public_ip:
                queryset.append({'id':asset.public_ip,'ip':asset.public_ip,'hostname':asset.hostname})
        return queryset