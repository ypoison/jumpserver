# -*- coding: utf-8 -*-
#
from django.views.generic import TemplateView, CreateView, \
    UpdateView, DetailView
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse_lazy

from common.permissions import AdminUserRequiredMixin
from common.const import create_success_msg

from ..models import Account
from ..forms import AccountForm


__all__ = (
    "AccountListView", "AccountDetailView","AccountCreateView", "AccountUpdateView",
)

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

