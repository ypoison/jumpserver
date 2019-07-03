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
from ..models import PlatformNode
from ..forms import PlatformNodeForm

__all__ = (
    "NodeListView", "NodeCreateView", "NodeDetailView",
    "NodeUpdateView",
)

class NodeListView(AdminUserRequiredMixin, TemplateView):
    template_name = 'node/node_list.html'

    def get_context_data(self, **kwargs):
        context = {
            'app': '配置管理',
            'action': '节点列表',
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

class NodeCreateView(AdminUserRequiredMixin, SuccessMessageMixin, CreateView):
    model = PlatformNode
    template_name = 'node/node_create_update.html'
    form_class = PlatformNodeForm
    success_url = reverse_lazy('config:high-nati-list')
    success_message = create_success_msg

    def get_context_data(self, **kwargs):
        context = {
            'app': '配置管理',
            'action': '添加节点信息',
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

class NodeDetailView(AdminUserRequiredMixin, DetailView):
    model = PlatformNode
    template_name = 'node/node_detail.html'

    def get_context_data(self, **kwargs):
        context = {
            'app': '配置管理',
            'action': '节点详情',
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

class NodeUpdateView(AdminUserRequiredMixin, SuccessMessageMixin, UpdateView):
    model = PlatformNode
    template_name = 'node/node_create_update.html'
    form_class = PlatformNodeForm
    success_url = reverse_lazy('config:high-anti-list')
    success_message = create_success_msg

    def get_context_data(self, **kwargs):
        context = {
            'app': '配置管理',
            'action': '节点更新',
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)