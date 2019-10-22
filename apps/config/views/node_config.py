# -*- coding: utf-8 -*-
#
from django.views.generic import TemplateView, CreateView, \
    UpdateView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from common.permissions import AdminUserRequiredMixin
from common.const import create_success_msg

from assets.models import Node
from ..models import WEBConfigRecords, App
from ..forms import WEBConfigForm, WEBConfigBulkForm, AppForm
from ..webconfig import WEBConfig
from ..tasks import bulk_config

__all__ = (
    "NodeConfigListView", "NodeConfigWEBConfigListView", "NodeConfigWEBConfigCreateView", "WEBConfigBulkCreateView",
    'AppListView', 'AppCreateView', 'AppUpdateView',
)
webconfig = WEBConfig()

class NodeConfigListView(LoginRequiredMixin, TemplateView):
    template_name = 'config/node_config_list.html'

    def get_context_data(self, **kwargs):
        context = {
            'app': '配置管理',
            'action': '节点信息列表',
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

class NodeConfigWEBConfigListView(LoginRequiredMixin, TemplateView):
    template_name = 'config/web_config_list.html'

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
    template_name = 'config/web_config_create_update.html'
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
            'ports': App.objects.all()
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

class WEBConfigBulkCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = WEBConfigRecords
    template_name = 'config/web_config_bulk_create.html'
    form_class = WEBConfigBulkForm
    success_url = reverse_lazy('config:web-config-list')
    success_message = "updated successfully."

    def form_valid(self, form):
        games = self.request.POST.getlist('Games')
        req = form.cleaned_data
        req['games'] = games
        job = bulk_config.delay(req)
        self.success_message = '配置任务已生成。 jobID: %s' % str(job).replace('-', '')
        messages.success(self.request, self.success_message)
        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = {
            'app': '配置管理',
            'action': '添加WEB配置',
            'ports': App.objects.all(),
            'games': App.objects.filter(type='game')
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class AppListView(AdminUserRequiredMixin, TemplateView):
    template_name = 'config/app_list.html'

    def get_context_data(self, **kwargs):
        context = {
            'app': '配置管理',
            'action': '应用信息列表',
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

class AppCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = App
    template_name = 'config/app_update.html'
    form_class = AppForm
    success_url = reverse_lazy('config:app-list')
    success_message = create_success_msg

    def get_context_data(self, **kwargs):
        context = {
            'app': '配置管理',
            'action': '应用信息创建',
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

class AppUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = App
    template_name = 'config/app_update.html'
    form_class = AppForm
    success_url = reverse_lazy('config:app-list')
    success_message = create_success_msg

    def get_context_data(self, **kwargs):
        context = {
            'app': '配置管理',
            'action': '应用信息更新',
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)