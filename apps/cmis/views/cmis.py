# -*- coding: utf-8 -*-
#
from django.views.generic import TemplateView, CreateView, \
    UpdateView, DetailView, FormView
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse_lazy
from django.shortcuts import redirect

from common.permissions import AdminUserRequiredMixin
from common.const import create_success_msg

from assets.models import Asset

from ..models import Account
from ..forms import AccountForm, CreateCHostForm
from .. import ucloud_api

import base64

__all__ = (
    "AccountListView", "AccountDetailView","AccountCreateView", "AccountUpdateView",
    "CHostCreateView",
)
cloud_api = ucloud_api.UcloudAPI()


class AccountCreateView(AdminUserRequiredMixin, SuccessMessageMixin, CreateView):
    model = Account
    template_name = 'cmis/account_create_update.html'
    form_class = AccountForm
    success_url = reverse_lazy('cmis:account-list')
    success_message = create_success_msg

    def get_context_data(self, **kwargs):
        context = {
            'app': '云管中心',
            'action': '添加账号',
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

class AccountUpdateView(AdminUserRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Account
    template_name = 'cmis/account_create_update.html'
    form_class = AccountForm
    success_url = reverse_lazy('cmis:account-list')
    success_message = create_success_msg

    def get_context_data(self, **kwargs):
        context = {
            'app': '云管中心',
            'action': '更新账号',
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

class AccountListView(AdminUserRequiredMixin, TemplateView):
    template_name = 'cmis/account_list.html'

    def get_context_data(self, **kwargs):
        context = {
            'app': _('云管中心'),
            'action': _('账号列表'),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

class AccountDetailView(AdminUserRequiredMixin, DetailView):
    model = Account
    template_name = 'cmis/account_detail.html'

    def get_context_data(self, **kwargs):
        context = {
            'app': _('云管中心'),
            'action': _('账号详情'),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

class CHostCreateView(AdminUserRequiredMixin, SuccessMessageMixin, FormView):
    template_name = 'cmis/chost_create.html'
    form_class = CreateCHostForm
    success_url = reverse_lazy('cmis:chost-create')
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

        passwd = base64.b64encode(req.get('passwd').encode('utf-8')).decode('utf-8')

        data = {
            'PrivateKey': account.access_key,
            "PublicKey": account.access_id,

            'Region': req.get('region'),
            'Zone':  req.get('zone'),
            'ProjectId':  req.get('project'),
            'ImageId': req.get('image'),
            'Name': req.get('name'),
            'LoginMode': 'Password',
            'Password': passwd,

            'CPU': req.get('cpu'),
            'Memory': req.get('memory'),
            'Disks.0.Type': req.get('disks0_type'),
            'Disks.0.IsBoot':True,
            'Disks.0.Size': req.get('disks0_size'),

            'ChargeType': req.get('charge_type'),
            'UHostType': req.get('host_type'),
            'NetCapability': req.get('net_capability'),
            'VPCId': req.get('vpc'),
            'SubnetId': req.get('subnet'),


        }
        if req.get('disks1_type'):
            data['Disks.1.Type'] = req.get('disks1_type')
            data['Disks.1.IsBoot'] = False
            data['Disks.1.Size'] = req.get('disks1_size')

        eip = req.get('eip', '')
        if eip == 'on':
            if req.get('region')[:2] == 'cn':
                data['NetworkInterface.0.EIP.OperatorName'] = 'Bgp'
            else:
                data['NetworkInterface.0.EIP.OperatorName'] = 'International'
            data['NetworkInterface.N.EIP.Bandwidth'] = req.get('eip_bandwidth')
            data['NetworkInterface.N.EIP.PayMode'] = req.get('eip_pay_mode')

        queryset = cloud_api.CreateUhostInstance(**data)
        if queryset['code']:
            data = queryset['msg']
            public_ip = data['IPs'][0]
            cid = data['UHostIds'][0]
        return redirect(self.success_url)