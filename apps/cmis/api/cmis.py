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
        action = self.request.data.get('action')
        account_id = self.request.data.get('account_id')
        if not id:
            return queryset
        account = Account.objects.get(id=account_id)
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
            project_id = self.request.data.get('project_id')
            region = self.request.data.get('region')
            zone  = self.request.data.get('zone')
            os_type = self.request.data.get('os_type')
            image_type = self.request.data.get('image_type')
            data['project_id'] = project_id
            data['Region'] = region
            data['Zone'] = zone
            data['OsType'] = os_type
            data['ImageType'] = image_type
            queryset = cloud_api.GetImageList(**data)
        else:
            queryset = []
        print(queryset)
        return Response(queryset)