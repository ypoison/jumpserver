# -*- coding: utf-8 -*-
#
from django.views.generic import TemplateView, CreateView, \
    UpdateView, DeleteView, DetailView, ListView
from django.views.generic.detail import SingleObjectMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy, reverse

from common.permissions import AdminUserRequiredMixin
from common.const import create_success_msg, update_success_msg
from common.utils import get_object_or_none
from assets.models import Node
from ..forms import PlatformNodeConfigForm

__all__ = (
    "NodeRecordListView", "NodeConfigCreateView", "NodeDetailView",
    "NodeUpdateView",
)

class NodeRecordListView(AdminUserRequiredMixin, TemplateView):
    template_name = 'node/node_record_list.html'

    def get_context_data(self, **kwargs):
        context = {
            'app': '配置管理',
            'action': '节点配置列表',
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

class NodeConfigCreateView(AdminUserRequiredMixin, SuccessMessageMixin, CreateView):
    model = Node
    template_name = 'node/node_config_create_update.html'
    form_class = PlatformNodeConfigForm
    success_url = reverse_lazy('config:node-record-list')
    success_message = "updated successfully."

    def get_context_data(self, **kwargs):
        context = {
            'app': '配置管理',
            'action': '添加节点信息',
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

    def get_form_kwargs(self):
        kwargs = super(NodeConfigCreateView, self).get_form_kwargs()
        data = {'request': self.request}
        kwargs.update(data)
        return kwargs

class NodeDetailView(AdminUserRequiredMixin, DetailView):
    model = Node
    template_name = 'node/node_detail.html'

    def get_context_data(self, **kwargs):
        context = {
            'app': '配置管理',
            'action': '节点详情',
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

class NodeUpdateView(AdminUserRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Node
    template_name = 'node/node_create_update.html'
    form_class = PlatformNodeConfigForm
    success_url = reverse_lazy('config:high-anti-list')
    success_message = "<b>%(value)s</b> was updated successfully."


    def get_context_data(self, **kwargs):
        context = {
            'app': '配置管理',
            'action': '节点更新',
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)