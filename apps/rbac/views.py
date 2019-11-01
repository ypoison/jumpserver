# -*- coding: utf-8 -*-
#
from django.views.generic import TemplateView, CreateView, \
    UpdateView, DetailView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy

from common.permissions import PermissionsMixin, IsOrgAdmin
from common.const import create_success_msg

from .models import Menu, Permission2User, Permission2Group
from .forms import MenuCreateForm, MenuUpdateForm, Permission2UserForm, Permission2GroupForm

from users.models import User, UserGroup

__all__ = (
    "MenuListView","MenuCreateView","MenuUpdateView",
    "GroupListView",
    "UserListView",
)

class MenuListView(PermissionsMixin, TemplateView):
    permission_classes = [IsOrgAdmin]
    template_name = 'rbac/menu_list.html'

    def get_context_data(self, **kwargs):
        context = {
            'app': 'rbac',
            'action': '菜单列表',
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class MenuCreateView(PermissionsMixin, SuccessMessageMixin, CreateView):
    model = Menu
    permission_classes = [IsOrgAdmin]
    template_name = 'rbac/menu_create_update.html'
    form_class = MenuCreateForm
    success_url = reverse_lazy('rbac:menu-list')
    success_message = create_success_msg

    def get_context_data(self, **kwargs):
        context = {
            'app': 'rbac',
            'action': '菜单添加',
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class MenuUpdateView(PermissionsMixin, SuccessMessageMixin, UpdateView):
    model = Menu
    permission_classes = [IsOrgAdmin]
    template_name = 'rbac/menu_create_update.html'
    form_class = MenuUpdateForm
    success_url = reverse_lazy('rbac:menu-list')
    success_message = create_success_msg

    def get_context_data(self, **kwargs):
        context = {
            'app': 'rbac',
            'action': '菜单更新',
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

class GroupListView(PermissionsMixin, TemplateView):
    permission_classes = [IsOrgAdmin]
    template_name = 'rbac/user_group_list.html'

    def get_context_data(self, **kwargs):
        context = {
            'app': 'rbac',
            'action': '用户组',
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

class UserListView(PermissionsMixin, TemplateView):
    permission_classes = [IsOrgAdmin]
    template_name = 'rbac/user_list.html'

    def get_context_data(self, **kwargs):
        context = {
            'app': 'rbac',
            'action': '用户',
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)