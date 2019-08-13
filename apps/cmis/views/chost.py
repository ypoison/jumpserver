# -*- coding: utf-8 -*-
#
from django.views.generic import TemplateView, FormView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from django import forms

from django.shortcuts import redirect

from common.permissions import AdminUserRequiredMixin
from common.const import create_success_msg
from common.utils import get_object_or_none

from assets.models import Asset,AdminUser,Node

from ..models import Account, ChostCreateRecord
from ..forms import CreateCHostForm

from ..tasks import buyer
import base64

__all__ = (
    "CHostCreateView", "CHostCreateRecordView",
)


class CHostCreateView(LoginRequiredMixin, SuccessMessageMixin, FormView):
    template_name = 'cmis/chost_create.html'
    form_class = CreateCHostForm
    success_url = reverse_lazy('cmis:chost-create-record-list')

    def get_context_data(self, **kwargs):
        context = {
            'app': '云管中心',
            'action': '采购云主机',
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        req = form.cleaned_data
        account = req.pop('account')
        Password = base64.b64encode(req.get('Password').encode('utf-8')).decode('utf-8')
        data = {
            'PrivateKey': account.access_key,
            "PublicKey": account.access_id,
            'LoginMode': 'Password',
            'Password': Password,

            'Disks.0.Type': req.pop('Disks0Type'),
            'Disks.0.IsBoot':True,
            'Disks.0.Size': req.pop('Disks0Size'),

            'UHostType': req.pop('HostType'),
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
        kw = {**req, **data}
        create_record = ChostCreateRecord.objects.create(
            region=kw['Region'],
            account_id=str(account.id)
        )
        buyer.delay(create_record, **kw)
        self.success_message = '采购任务已生成。 jobID: %s' % str(create_record.id).replace('-','')
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