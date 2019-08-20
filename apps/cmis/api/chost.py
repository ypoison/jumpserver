# ~*~ coding: utf-8 ~*~
from rest_framework_bulk import BulkModelViewSet
from rest_framework.views import Response
from rest_framework.generics import ListAPIView
from rest_framework.pagination import LimitOffsetPagination
from common.utils import get_logger, get_object_or_none
from common.permissions import IsOrgAdmin, IsValidUser

from ..models import Account, ChostCreateRecord, ChostModel
from .. import serializers

from .. import ucloud_api

from ..tasks import set_info

logger = get_logger(__file__)
__all__ = [
            'CloudInfoAPI', 'ChostCreateRecordAPI', 'GetStatusAPI',
            'GetPriceAPI', 'SetModelAPI', 'ForModelAPI','CreateIsolationGroupAPI',
        ]
cloud_api = ucloud_api.UcloudAPI()

class CloudInfoAPI(ListAPIView):
    permission_classes = (IsValidUser,)

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
        elif action == 'DescribeUHostTags':
            queryset = cloud_api.GetUHostTags(**data)
        elif action == 'DescribeIsolationGroup':
            queryset = cloud_api.DescribeIsolationGroup(**data)
        else:
            return Response({'error': 'action参数错误'}, status=400)
        if queryset['code']:
            return Response(queryset)
        else:
            return Response(queryset, status=400)

class ChostCreateRecordAPI(ListAPIView):
    filter_fields = ("id", "hid")
    search_fields = filter_fields
    queryset = ChostCreateRecord.objects.all()
    permission_classes = (IsValidUser,)
    serializer_class = serializers.ChostCreateRecordSerializer
    pagination_class = LimitOffsetPagination

class GetStatusAPI(ListAPIView):
    permission_classes = (IsValidUser,)

    def get(self, request, *args, **kwargs):
        record_id = self.kwargs.get('pk')
        record = get_object_or_none(ChostCreateRecord, id=record_id)
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

class GetPriceAPI(ListAPIView):
    permission_classes = (IsValidUser,)

    def post(self, request, *args, **kwargs):
        req = self.request.data
        account_id = req.pop('account')
        try:
            account = get_object_or_none(Account, id=account_id)
            data = {
                'PrivateKey': account.access_key,
                'PublicKey': account.access_id,
                'Count': 1,
                'Disks.0.Type': req.pop('Disks0Type'),
                'Disks.0.IsBoot': True,
                'Disks.0.Size': int(req.pop('Disks0Size')),
                'ProjectId': req['ProjectId'],
                'ChargeType': req['ChargeType'],
                'Region': req['Region'],
                'Zone': req['Zone'],
                'ImageId': req['ImageId'],
                'MachineType': req['MachineType'],
                'CPU': int(req['CPU']),
                'Memory': int(req['Memory']),
                'NetCapability': req['NetCapability'],
            }
            Disks1Type = req.pop('Disks1Type')
            if Disks1Type:
                data['Disks.1.Type'] = Disks1Type
                data['Disks.1.IsBoot'] = False
                data['Disks.1.Size'] = int(req.pop('Disks1Size'))

            if not data.get('ChargeType') == 'Dynamic':
                data['Quantity'] = int(req['Quantity'])

            host_price = cloud_api.GetUHostInstancePrice(**data)['msg']
            if req.get('EIP', ''):
                data = {
                    'PrivateKey': account.access_key,
                    'PublicKey': account.access_id,
                    'Region': req['Region'],
                    'ProjectId': req['ProjectId'],
                    'Bandwidth': req['EIPBandwidth'],
                    'ChargeType': req['ChargeType'],
                    'PayMode': req['EIPPayMode']
                }
                if not data.get('ChargeType') == 'Dynamic':
                    data['Quantity'] = int(req['Quantity'])
                if req.get('Region')[:2] == 'cn':
                    data['OperatorName'] = 'Bgp'
                else:
                    data['OperatorName'] = 'International'
                EIP_price = cloud_api.GetEIPPrice(**data)['msg']
            else:
                EIP_price = 0
            try:
                sum = '%.2f' % (host_price + EIP_price)
                host_price = '%.2f' % host_price
                EIP_price = '%.2f' % EIP_price
            except:
                sum = 0
            queryset = {'host_price':host_price, 'EIP_price':EIP_price, 'sum':sum}
        except:
            queryset = {}
        return Response(queryset)

class SetModelAPI(ListAPIView):
    permission_classes = (IsValidUser,)

    def post(self, request, *args, **kwargs):
        req = self.request.data
        data = {
            'name': req['model_name'],
            'charge_type': req['ChargeType'],
            'quantity': int(req['Quantity']),
            'machine_type': req['MachineType'],
            'net_capability': req['NetCapability'],
            'cpu': int(req['CPU']),
            'memory': int(req['Memory']),

            'disks_0_type': req.pop('Disks0Type'),
            'disks_0_size': int(req.pop('Disks0Size')),
            'disks_1_type': req.get('Disks1Type', ''),

            'eip_bandwidth': req.get('EIPBandwidth', ''),
            'eip_pay_mode': req.get('EIPPayMode', ''),
            'ssh_port': req['SSHPort'],
            'region': req.get('Region'),
            'zone': req.get('Zone'),
            'vpc': req.get('VPCId'),
            'subnet': req.get('SubnetId'),
            'security_group': req.get('SecurityGroupId'),
            'os_type': req.get('OSType'),
            'image_type': req.get('ImageType'),
            'image': req.get('ImageId')


        }
        if req.get('HotplugFeature', ''):
            data['hotplug_feature'] = True
        if req.get('EIP', ''):
            data['eip'] = True
        if req.get('Disks1Size', ''):
            data['disks_1_size'] = int(req.get('Disks1Size'))
        try:
            ChostModel.objects.create(**data)
            models = ChostModel.objects.all()
            print(models)
            smodels = serializers.ChostModelSerializer(models, many=True)
            return Response(smodels.data)
        except Exception as e:
            return Response({'error': '模板添加失败：%s' % e}, status=400)

class ForModelAPI(ListAPIView):
    permission_classes = (IsValidUser,)

    def get(self, request, *args, **kwargs):
        model_id = self.kwargs.get('pk')
        model = get_object_or_none(ChostModel, id=model_id)
        if not model:
            return Response({'error': '模板不存在'}, status=400)
        queryset = serializers.ChostModelSerializer(model)
        print(queryset.data)
        return Response(queryset.data)

class CreateIsolationGroupAPI(ListAPIView):
    permission_classes = (IsValidUser,)

    def post(self, request, *args, **kwargs):
        data = self.request.data
        accountId = data.pop('accountId')
        try:
            account = get_object_or_none(Account, id=accountId)
        except Exception as e:
            return Response({'code': 0, 'error': '账户信息错误：' % e}, status=400)
        if not account:
            return Response({'code': 0, 'error': '找不到账户信息'}, status=400)
        data.update({
            'PrivateKey': account.access_key,
            "PublicKey": account.access_id,
        })
        queryset = cloud_api.CreateIsolationGroup(**data)
        if queryset['code']:
            return Response(queryset)
        else:
            return Response(queryset, status=400)