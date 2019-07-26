# ~*~ coding: utf-8 ~*~
from rest_framework.views import Response
from rest_framework_bulk import BulkModelViewSet
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.generics import ListAPIView

from common.utils import get_logger, get_object_or_none
from common.permissions import IsOrgAdmin

from ..models import Account
from .. import serializers

from .. import ucloud_api

logger = get_logger(__file__)
__all__ = ['AccountViewSet', 'CloudInfoAPI']
cloud_api = ucloud_api.UcloudAPI()

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

class CloudInfoAPI(ListAPIView):
    permission_classes = (IsOrgAdmin,)
    serializer_class = serializers.AccountSerializer

    def post(self, request, *args, **kwargs):
        queryset = []
        action = self.request.data.get('action')
        account_id = self.request.data.get('account_id')
        try:
            account = get_object_or_none(Account, id=account_id)
        except Exception as e:
            return Response({'code':0, 'msg':e})
        if not account:
            return Response({'code':0, 'msg':queryset})
        data = {
            'PrivateKey': account.access_key,
            "Action": action,
            "PublicKey": account.access_id,
        }
        if action == 'getproject':
            queryset = cloud_api.GetProjectList(**data)
        elif action == 'getregion':
            queryset = cloud_api.GetRegion(**data)
        elif action == 'getzone':
            region = self.request.data.get('region')
            data['Region'] = region
            queryset = cloud_api.GetZone(**data)
        elif action == 'getimage':
            region = self.request.data.get('region')
            zone = self.request.data.get('zone')
            os_type = self.request.data.get('os_type')
            image_type = self.request.data.get('image_type')
            data['Region'] = region
            data['Zone'] = zone
            data['OsType'] = os_type
            data['ImageType'] = image_type
            queryset = cloud_api.GetImageList(**data)
        elif action == 'getVPC':
            project_id = self.request.data.get('project_id')
            region = self.request.data.get('region')
            data['Region'] = region
            data['ProjectId'] = project_id
            queryset = cloud_api.GetVPC(**data)
        elif action == 'getsubnet':
            project_id = self.request.data.get('project_id')
            region = self.request.data.get('region')
            vpc_id = self.request.data.get('vpc_id')
            data['Region'] = region
            data['ProjectId'] = project_id
            data['vpc_id'] = vpc_id
            queryset = cloud_api.GetSubnet(**data)
        else:
            queryset = []
        return Response(queryset)