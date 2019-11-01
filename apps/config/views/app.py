# -*- coding: utf-8 -*-
#
from django.views.generic import TemplateView, CreateView, \
    UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy

from common.permissions import PermissionsMixin, IsOrgAdmin, IsValidUser
from django.contrib.auth.mixins import LoginRequiredMixin
from common.const import create_success_msg

from ..models import App
from ..forms import AppForm

__all__ = (
    'AppListView', 'AppCreateView', 'AppUpdateView',
)

class AppListView(LoginRequiredMixin, TemplateView):
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
    template_name = 'config/app_create_update.html'
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
    template_name = 'config/app_create_update.html'
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