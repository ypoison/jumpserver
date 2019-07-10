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
from ..models import WEBConfigRecords
from ..forms import PlatformNodeConfigForm, WEBConfigForm
from ..webconfig import WEBConfig

__all__ = (
    "NodeConfigListView", "NodeConfigCreateView",
    "NodeConfigWEBConfigListView", "NodeConfigWEBConfigCreateView"
)
webconfig = WEBConfig()

class NodeConfigListView(AdminUserRequiredMixin, TemplateView):
    template_name = 'node_config/node_config_list.html'

    def get_context_data(self, **kwargs):
        context = {
            'app': '配置管理',
            'action': '节点信息列表',
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

class NodeConfigCreateView(AdminUserRequiredMixin, SuccessMessageMixin, CreateView):
    model = Node
    template_name = 'node_config/node_config_create_update.html'
    form_class = PlatformNodeConfigForm
    success_url = reverse_lazy('config:node-config-list')
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

class NodeConfigWEBConfigListView(AdminUserRequiredMixin, TemplateView):
    template_name = 'node_config/web_config_list.html'

    def get_context_data(self, **kwargs):
        context = {
            'app': '配置管理',
            'action': '节点WEB配置',
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

class NodeConfigWEBConfigCreateView(AdminUserRequiredMixin, SuccessMessageMixin, CreateView):
    model = WEBConfigRecords
    template_name = 'node_config/web_config_create_update.html'
    form_class = WEBConfigForm
    success_url = reverse_lazy('config:web-config-list')
    success_message = "updated successfully."

    def form_valid(self, form):
        web_config = form.save(commit=False)
        print(web_config.__dict__)
        #add_web_config = webconfig.add(record)
        #if add_record['code']:
        #    add_record = add_record['message']
        #    record.record_id = add_record['RecordId']
        #    record.save()
        #else:
        #    form.add_error(
        #        "record_id", add_record['message']
        #    )
        #    return self.form_invalid(form)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = {
            'app': '配置管理',
            'action': '添加WEB配置',
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)