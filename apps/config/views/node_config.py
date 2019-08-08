# -*- coding: utf-8 -*-
#
from django.views.generic import TemplateView, CreateView, \
    UpdateView, DeleteView, DetailView, ListView
from django.views.generic.detail import SingleObjectMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy, reverse

from common.permissions import AdminUserRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from common.const import create_success_msg, update_success_msg
from common.utils import get_object_or_none
from assets.models import Node
from ..models import WEBConfigRecords
from ..forms import WEBConfigForm
from ..webconfig import WEBConfig

__all__ = (
    "NodeConfigListView", "NodeConfigWEBConfigListView", "NodeConfigWEBConfigCreateView"
)
webconfig = WEBConfig()

class NodeConfigListView(LoginRequiredMixin, TemplateView):
    template_name = 'node_config/node_config_list.html'

    def get_context_data(self, **kwargs):
        context = {
            'app': '配置管理',
            'action': '节点信息列表',
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

class NodeConfigWEBConfigListView(LoginRequiredMixin, TemplateView):
    template_name = 'node_config/web_config_list.html'

    def get_context_data(self, **kwargs):
        context = {
            'app': '配置管理',
            'action': '节点WEB配置',
            'platforms': Node.objects.filter(key__regex=r'^1:[0-9]$|[0-9][0-9]$|[0-9][0-9][0-9]$').exclude(code="GGDLJD")
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

class NodeConfigWEBConfigCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = WEBConfigRecords
    template_name = 'node_config/web_config_create_update.html'
    form_class = WEBConfigForm
    success_url = reverse_lazy('config:web-config-list')
    success_message = "updated successfully."

    def form_valid(self, form):
        web_config = form.save(commit=False)
        kwargs = (web_config.__dict__)
        node_ip = web_config.node_asset.ip
        kwargs.update(node_ip=node_ip)
        platform = web_config.platform.code
        kwargs.update(platform=platform)
        add_web_config = webconfig.add(**kwargs)
        if add_web_config['code']:
            web_config.save()
        else:
            form.add_error(
                "domain", add_web_config['msg']
            )
            return self.form_invalid(form)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = {
            'app': '配置管理',
            'action': '添加WEB配置',
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)