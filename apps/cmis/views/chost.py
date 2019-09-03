# -*- coding: utf-8 -*-
#
from django.views.generic import TemplateView, FormView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.forms.forms import NON_FIELD_ERRORS
from common.utils import get_object_or_none

from assets.models import Asset, Node

from ..models import ChostCreateRecord, ChostModel
from config.models import App
from ..forms import CHostCreateForm, CHostBulkCreateForm

from ..tasks import buyer, bulk_buyer
import base64

from .. import ucloud_api
cloud_api = ucloud_api.UcloudAPI()
__all__ = (
    "CHostCreateView", "CHostBulkCreateView",
    "CHostCreateRecordView",
)

class CHostCreateView(LoginRequiredMixin, SuccessMessageMixin, FormView):
    template_name = 'cmis/chost_create.html'
    form_class = CHostCreateForm
    success_url = reverse_lazy('cmis:chost-create-record-list')

    def get_context_data(self, **kwargs):
        context = {
            'app': '云管中心',
            'action': '采购云主机',
            'models': ChostModel.objects.all()
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        req = form.cleaned_data
        check_asset = get_object_or_none(Asset, hostname=req.get('Name'))
        if check_asset:
            form.add_error(
                "Name", "资产已经存在该hostname主机。"
            )
            return self.form_invalid(form)
        account = req.pop('account')
        Password = base64.b64encode(req.get('Password').encode('utf-8')).decode('utf-8')
        data = {
            'PrivateKey': account.access_key,
            "PublicKey": account.access_id,
            'LoginMode': 'Password',
            'Password': Password,
            'MinimalCpuPlatform': 'Intel/Auto',
            'Disks.0.Type': req.pop('Disks0Type'),
            'Disks.0.IsBoot':True,
            'Disks.0.Size': req.pop('Disks0Size'),
        }

        Disks1Type = req.pop('Disks1Type')
        if Disks1Type:
            data['Disks.1.Type'] = Disks1Type
            data['Disks.1.IsBoot'] = False
            data['Disks.1.Size'] = req.pop('Disks1Size')
        else:
            del req['Disks1Size']

        if req.pop('EIP', ''):
            if req.get('Region')[:2] == 'cn':
                data['NetworkInterface.0.EIP.OperatorName'] = 'Bgp'
            else:
                data['NetworkInterface.0.EIP.OperatorName'] = 'International'
            data['NetworkInterface.0.EIP.Bandwidth'] = req.pop('EIPBandwidth')
            data['NetworkInterface.0.EIP.PayMode'] = req.pop('EIPPayMode')
        else:
            del req['EIPBandwidth']
            del req['EIPPayMode']

        if req.get('ChargeType') == 'Dynamic':
            del req['Quantity']

        kw = {**req, **data}
        create_record = ChostCreateRecord.objects.create(
            region=kw['Region'],
            account_id=str(account.id)
        )
        buyer.delay(create_record, **kw)
        self.success_message = '采购任务已生成。 jobID: %s' % str(create_record.id).replace('-','')
        return super().form_valid(form)

class CHostBulkCreateView(LoginRequiredMixin, SuccessMessageMixin, FormView):
    template_name = 'cmis/chost_bulk_create.html'
    form_class = CHostBulkCreateForm
    success_url = reverse_lazy('cmis:chost-create-record-list')

    def get_context_data(self, **kwargs):
        context = {
            'app': '云管中心',
            'action': '批量采购云主机',
            'models': ChostModel.objects.all(),
            'names': App.objects.filter(type='game')
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        create_host_list = self.request.POST.getlist('Name')
        if not create_host_list:
            create_host_list = [i.name for i in App.objects.filter(type='game')]
        req = form.cleaned_data
        try:
            node_key = req.get('nodes')[0].key[:3]
            node_code = Node.objects.get(key=node_key).code
        except:
            form.add_error(
                "nodes", "获取节点别名失败。"
            )
            return self.form_invalid(form)
        model = req.pop('chost_model')
        account = req.get('account')
        # ImageId
        getImage = {
            'PrivateKey': account.access_key,
            'PublicKey': account.access_id,
            'Region': req.get('Region'),
            'Zone': req.get('Zone'),
            'ImageType': model.image_type,
            'OsType': model.os_type
        }
        queryset = cloud_api.GetImageList(**getImage)
        if queryset:
            ImageId = ''
            for image in queryset['msg']:
                if image['name'] == model.image:
                    ImageId = image.get('id')
                    break
            if not ImageId:
                form._errors[NON_FIELD_ERRORS] = form.error_class(['获取镜像信息失败,请检查该地区是否有改镜像。'])
                return self.form_invalid(form)
        else:
            form._errors[NON_FIELD_ERRORS] = form.error_class(['获取镜像信息失败'])
            return self.form_invalid(form)
        # ImageId end

        # VPCId
        getData = {
            'PrivateKey': account.access_key,
            'PublicKey': account.access_id,
            'Region': req.get('Region'),
            'ProjectId': req.get('ProjectId'),
        }
        queryset = cloud_api.GetVPC(**getData)
        try:
            for i in queryset['msg']:
                if i['name'] == model.vpc:
                    VPCId = i['id']
        except:
            form._errors[NON_FIELD_ERRORS] = form.error_class(['获取VPC信息失败'])
            return self.form_invalid(form)

        getData['VPCId'] = VPCId
        queryset = cloud_api.GetSubnet(**getData)
        try:
            for i in queryset['msg']:
                if i['name'] == model.subnet:
                    SubnetId = i['id']
        except:
            form._errors[NON_FIELD_ERRORS] = form.error_class(['获取VPC信息失败'])
            return self.form_invalid(form)

        # VPCId end

        Password = base64.b64encode(req.get('Password').encode('utf-8')).decode('utf-8')
        data = {
            'account':account,
            'PrivateKey': account.access_key,
            'PublicKey': account.access_id,
            'SSHPort': model.ssh_port,
            'ChargeType': model.charge_type,
            'Region': req.get('Region'),
            'Zone': req.get('Zone'),
            'ProjectId': req.get('ProjectId'),
            'MachineType': model.machine_type,
            'NetCapability': model.net_capability,
            'HotplugFeature': model.hotplug_feature,
            'CPU': model.cpu,
            'Memory': model.memory,
            'OSType': model.os_type,
            'ImageId': ImageId,
            'VPCId': VPCId,
            'SubnetId': SubnetId,
            'SecurityGroupId': req.get('SecurityGroupId'),
            'LoginMode': 'Password',
            'Password': Password,
            'MinimalCpuPlatform': 'Intel/Auto',
            'Disks.0.Type': model.disks_0_type,
            'Disks.0.IsBoot': True,
            'Disks.0.Size': model.disks_0_size,
        }
        Disks1Type = model.disks_1_type
        if Disks1Type:
            data['Disks.1.Type'] = Disks1Type
            data['Disks.1.IsBoot'] = False
            data['Disks.1.Size'] = model.disks_1_size
        if model.eip:
            if req.get('Region')[:2] == 'cn':
                data['NetworkInterface.0.EIP.OperatorName'] = 'Bgp'
            else:
                data['NetworkInterface.0.EIP.OperatorName'] = 'International'
            data['NetworkInterface.0.EIP.Bandwidth'] = model.eip_bandwidth
            data['NetworkInterface.0.EIP.PayMode'] = model.eip_pay_mode
        if model.charge_type != 'Dynamic':
            data['Quantity'] = model.quantity
        if req.get('IsolationGroup',''):
            data['IsolationGroup'] = req.get('IsolationGroup')
        if req.get('Tag',''):
            data['Tag'] = req.get('Tag')

        job = bulk_buyer.delay(node_code, create_host_list, req, **data)
        self.success_message = '采购任务已生成。 jobID: %s' % str(job).replace('-', '')
        return super().form_valid(form)

class CHostCreateRecordView(LoginRequiredMixin, TemplateView):
    template_name = 'cmis/chost_create_record_list.html'

    def get_context_data(self, **kwargs):
        context = {
            'app': '云管中心',
            'action': '云主机采购记录',
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)