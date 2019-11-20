# ~*~ coding: utf-8 ~*~

from rest_framework import generics
from rest_framework_bulk import BulkModelViewSet
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.views import APIView, Response
from django.shortcuts import get_object_or_404

from common.mixins import IDInFilterMixin
from common.utils import get_logger, get_object_or_none
from common.permissions import IsValidUser

from ..models import Records, RecordsTree
from .. import serializers

from assets.models import Node

logger = get_logger(__file__)
__all__ = ['RecordsViewSet','RecordsUpdateApi', 'RecordsPlatformAsTreeApi']

class RecordsViewSet(IDInFilterMixin, BulkModelViewSet):
    filter_fields = ('name','path')
    search_fields = filter_fields
    queryset = Records.objects.all()
    permission_classes = (IsValidUser,)
    serializer_class = serializers.RecordsSerializer
    pagination_class = LimitOffsetPagination

    def filter_tree(self, queryset):
        tree_id = self.request.query_params.get("tree_id")
        if not tree_id:
            return queryset

        record_tree = get_object_or_404(RecordsTree, id=tree_id)
        queryset = queryset.filter(
            path=record_tree.key,
        )
        return queryset

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        queryset = self.filter_tree(queryset)
        return queryset

class RecordsUpdateApi(APIView):
    permission_classes = (IsValidUser,)

    def post(self, request, *args, **kwargs):
        req = self.request.data
        path_list = []

        platform = req['platform']
        check_tree_root = get_object_or_none(RecordsTree, key='{}/'.format(platform))
        if not check_tree_root:
            platform_info = get_object_or_none(Node, code=platform)
            if platform_info:
                platform_value = platform_info.value
            else:
                return Response({"code": 0, "msg": "检查是否存在'{}'此平台！".format(platform)})
            RecordsTree.objects.create(key='{}/'.format(platform),value=platform_value)
            
        data = req['data']
        if data:
            for d in data:
                name = d.pop('name')
                path = d.pop('path')
    
                if path not in path_list:
                    path_list.append(path)
    
                Records.objects.update_or_create(platform=platform,name=name,path=path, defaults=d)
            for path in path_list:
                the_tree_list = path.split('/')[1:-1]
                n = len(the_tree_list)
                for i in range(n):
                    p = '/'.join(the_tree_list[:n])
                    the_tree_value = the_tree_list[n-1]
                    the_tree_key = '{}/{}/'.format(platform, p)
                    check_tree = get_object_or_none(RecordsTree,key=the_tree_key)
                    if check_tree:
                        break
                    RecordsTree.objects.create(key=the_tree_key,value=the_tree_value)
                    n -= 1
        return Response({"code": 1, "msg": "ok"})

class RecordsPlatformAsTreeApi(generics.ListAPIView):
    """
    节点子节点作为树返回，
    [
      {
        "id": "",
        "name": "",
        "pId": "",
        "meta": ""
      }
    ]

    """
    permission_classes = (IsValidUser,)
    serializer_class = serializers.TreeRecordSerializer
    is_root = False

    def get_queryset(self):
        node_key = self.request.query_params.get('key')
        if node_key:
            self.node = RecordsTree.objects.get(key=node_key)
            queryset = self.node.get_children()
        else:
            self.is_root = True
            queryset = RecordsTree.get_tree_root()
        queryset = [node.as_tree_node(self.is_root) for node in queryset]
        return queryset