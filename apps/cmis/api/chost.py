# ~*~ coding: utf-8 ~*~
from rest_framework_bulk import BulkModelViewSet
from rest_framework.views import Response
from rest_framework.generics import ListAPIView
from rest_framework.pagination import LimitOffsetPagination
from common.utils import get_logger, get_object_or_none
from common.permissions import IsOrgAdmin, IsValidUser

from ..models import Account, ChostCreateRecord
from .. import serializers

from .. import ucloud_api

from ..tasks import set_info

logger = get_logger(__file__)
__all__ = [
            'CloudInfoAPI', 'ChostCreateRecordAPI', 'GetStatusAPI',
        ]
cloud_api = ucloud_api.UcloudAPI()

class CloudInfoAPI(ListAPIView):
    permission_classes = (IsValidUser,)
    serializer_class = serializers.AccountSerializer

    def post(self, request, *args, **kwargs):
        queryset = []
        data = self.request.data
        action = data.get('Action')
        account_id = data.pop('account_id')
        try:
            account = get_object_or_none(Account, id=account_id)
        except Exception as e:
            return Response({'code':0, 'msg':e})
        if not account:
            return Response({'code':0, 'msg':queryset})
        data.update({
            'PrivateKey': account.access_key,
            "PublicKey": account.access_id,
        })
        if action == 'GetProjectList':
            queryset = cloud_api.GetProjectList(**data)
        elif action == 'GetRegion':
            queryset = cloud_api.GetRegion(**data)
        elif action == 'GetZone':
            queryset = cloud_api.GetZone(**data)
        elif action == 'DescribeImage':
            queryset = cloud_api.GetImageList(**data)
        elif action == 'DescribeVPC':
            queryset = cloud_api.GetVPC(**data)
        elif action == 'DescribeSubnet':
            queryset = cloud_api.GetSubnet(**data)
        elif action == 'DescribeUHostInstance':
            queryset = cloud_api.GetUHostInstance(**data)
        elif action == 'DescribeFirewall':
            queryset = cloud_api.GetFirewall(**data)
        else:
            queryset = []
        return Response(queryset)

class ChostCreateRecordAPI(ListAPIView):
    filter_fields = ("id", "hid")
    search_fields = filter_fields
    queryset = ChostCreateRecord.objects.all()
    permission_classes = (IsValidUser,)
    serializer_class = serializers.ChostCreateRecordSerializer
    pagination_class = LimitOffsetPagination

class GetStatusAPI(ListAPIView):
    permission_classes = (IsValidUser,)
    serializer_class = serializers.AccountSerializer

    def get(self, request, *args, **kwargs):
        record_id = self.kwargs.get('pk')
        print(record_id)
        record = get_object_or_none(ChostCreateRecord, id=record_id)
        print(record)
        account = record.account
        if not account:
            return Response({'error': '账号信息不存在'}, status=400)
        data = {
            'PrivateKey': account.access_key,
            "PublicKey": account.access_id,
            "Region": record.region,
            "UHostIds.0": record.hid
        }
        queryset = cloud_api.GetUHostInstance(**data)
        set_info(queryset)
        return Response(queryset)