# -*- coding: utf-8 -*-
#
from django.views.generic import TemplateView, FormView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from django.shortcuts import redirect

from common.permissions import AdminUserRequiredMixin
from common.const import create_success_msg
from common.utils import get_object_or_none

from assets.models import Asset,AdminUser,Node

from ..models import Account, ChostCreateRecord
from ..forms import CreateCHostForm
from .. import ucloud_api

import base64

__all__ = (
    "CHostCreateView", "CHostCreateRecordView",
)
cloud_api = ucloud_api.UcloudAPI()

class CHostCreateView(AdminUserRequiredMixin, SuccessMessageMixin, FormView):
    template_name = 'cmis/chost_create.html'
    form_class = CreateCHostForm
    success_url = reverse_lazy('cmis:chost-create-record-list')
    success_message = create_success_msg

    def get_context_data(self, **kwargs):
        context = {
            'app': '云管中心',
            'action': '采购云主机',
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        req = request.POST
        account_id = req.get('account')
        try:
            account = Account.objects.get(id=account_id)
        except Exception as e:
            return redirect(reverse_lazy('cmis:chost-create'))

        Password = base64.b64encode(req.get('Password').encode('utf-8')).decode('utf-8')
        data = {
            'PrivateKey': account.access_key,
            "PublicKey": account.access_id,

            'Region': req.get('Region'),
            'Zone':  req.get('Zone'),
            'ProjectId':  req.get('ProjectId'),
            'ImageId': req.get('ImageId'),
            'Name': req.get('Name'),
            'LoginMode': 'Password',
            'Password': Password,

            'CPU': req.get('CPU'),
            'Memory': req.get('Memory'),
            'Disks.0.Type': req.get('Disks0Type'),
            'Disks.0.IsBoot':True,
            'Disks.0.Size': req.get('Disks0Size'),

            'ChargeType': req.get('ChargeType'),
            'UHostType': req.get('HostType'),
            'NetCapability': req.get('NetCapability'),
            'VPCId': req.get('VPCId'),
            'SubnetId': req.get('SubnetId'),


        }

        if req.get('disks1_type'):
            data['Disks.1.Type'] = req.get('Disks1Type')
            data['Disks.1.IsBoot'] = False
            data['Disks.1.Size'] = req.get('Disks1Size')

        eip = req.get('EIP', '')
        if eip == 'on':
            if req.get('Region')[:2] == 'cn':
                data['NetworkInterface.0.EIP.OperatorName'] = 'Bgp'
            else:
                data['NetworkInterface.0.EIP.OperatorName'] = 'International'
            data['NetworkInterface.N.EIP.Bandwidth'] = req.get('EIPBandwidth')
            data['NetworkInterface.N.EIP.PayMode'] = req.get('EIPPayMode')
        queryset = cloud_api.CreateUhostInstance(**data)
        if queryset['code']:
            data = queryset['msg']
            public_ip = data['IPs'][0]
            cid = data['UHostIds'][0]
            admin_user = get_object_or_none(AdminUser, id=req.get('admin_user'))
            asset = Asset.objects.create(
                hostname=req.get('Name'),
                platform=req.get('OSType'),
                ip=public_ip,
                public_ip=public_ip,
                admin_user=admin_user,
                number=cid,
                comment='由云账号"%s"添加' % account,
                is_active=False,
            )
            nodes = []
            for node_id in req.getlist('nodes'):
                node = get_object_or_none(Node, id=node_id)
                nodes.append(node)
            asset.nodes.set(nodes)
            print(str(account.id))
            ChostCreateRecord.objects.create(
                account=str(account.id),
                hid=cid,
                asset=asset,
            )

        return redirect(self.success_url)

class CHostCreateRecordView(LoginRequiredMixin, TemplateView):
    template_name = 'cmis/chost_create_record_list.html'

    def get_context_data(self, **kwargs):
        context = {
            'app': '云管中心',
            'action': '云主机采购记录',
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)