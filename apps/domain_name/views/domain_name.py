# -*- coding: utf-8 -*-
#
from django.views.generic import TemplateView, CreateView, \
    UpdateView, DetailView
from django.views.generic.detail import SingleObjectMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse_lazy, reverse

from common.permissions import AdminUserRequiredMixin
from common.const import create_success_msg
from common.utils import get_object_or_none
from ..models import DomainName, Records, Account
from ..forms import DomainNameForm, DomainNameRecordForm, DomainNameAccountForm

from ..domain_name_api import DomainNameApi


__all__ = (
    "DomainNameListView", "DomainNameUpdateView",
    "DomainNameDetailView", "DomainNameRecordsListView", "DomainNameRecordCreateView",
    "DomainNameRecordUpdateView", "DomainNameAccountListView", "DomainNameAccountDetailView",
    "DomainNameAccountCreateView", "DomainNameAccountUpdateView", "DomainNameCreateView",
)
GetDomainName=DomainNameApi()


class DomainNameAccountCreateView(AdminUserRequiredMixin, SuccessMessageMixin, CreateView):
    model = Account
    template_name = 'domain_name/account_create_update.html'
    form_class = DomainNameAccountForm
    success_url = reverse_lazy('domain-name:account-list')
    success_message = create_success_msg

    def get_context_data(self, **kwargs):
        context = {
            'app': '域名管理',
            'action': '域名账号管理',
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

class DomainNameAccountUpdateView(AdminUserRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Account
    template_name = 'domain_name/account_create_update.html'
    form_class = DomainNameAccountForm
    success_url = reverse_lazy('domain-name:account-list')
    success_message = create_success_msg

    def get_context_data(self, **kwargs):
        context = {
            'app': '域名管理',
            'action': '域名账号管理',
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

class DomainNameAccountListView(AdminUserRequiredMixin, TemplateView):
    template_name = 'domain_name/account_list.html'

    def get_context_data(self, **kwargs):
        context = {
            'app': _('域名管理'),
            'action': _('域名账号列表'),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

class DomainNameAccountDetailView(AdminUserRequiredMixin, DetailView):
    model = DomainName
    template_name = 'domain_name/account_detail.html'

    def get_context_data(self, **kwargs):
        context = {
            'app': _('域名管理'),
            'action': _('域名账号详情'),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class DomainNameListView(AdminUserRequiredMixin, TemplateView):
    template_name = 'domain_name/domain_name_list.html'

    def get_context_data(self, **kwargs):
        context = {
            'app': _('域名管理'),
            'action': _('域名列表'),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

class DomainNameCreateView(AdminUserRequiredMixin, SuccessMessageMixin, CreateView):
    model = DomainName
    template_name = 'domain_name/domain_name_create.html'
    form_class = DomainNameForm
    success_url = reverse_lazy('domain-name:domain-name-list')
    success_message = "<b>%(domain_name)s</b> was updated successfully."

    def form_valid(self, form):
        domain = form.save(commit=False)

        add_domain = GetDomainName.domain_name_create(domain)

        if add_domain['code']:
            domain.save()
        else:
            form.add_error(
                "domain_name", add_domain['message']
            )
            return self.form_invalid(form)
        return super().form_valid(form)


    def get_context_data(self, **kwargs):
        context = {
            'app': '域名管理',
            'action': '添加域名',
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

class DomainNameUpdateView(AdminUserRequiredMixin, SuccessMessageMixin, UpdateView):
    model = DomainName
    template_name = 'domain_name/domain_name_update.html'
    form_class = DomainNameForm
    success_url = reverse_lazy('domain-name:domain-name-list')
    success_message = "<b>%(domain_name)s</b> was updated successfully."

    def form_valid(self, form):
        print(form.errors)
        return super().form_valid(form)



    def get_context_data(self, **kwargs):
        context = {
            'app': '域名管理',
            'action': '更新域名',
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

class DomainNameDetailView(AdminUserRequiredMixin, DetailView):
    model = DomainName
    template_name = 'domain_name/domain_name_detail.html'

    def get_context_data(self, **kwargs):
        context = {
            'app': _('域名管理'),
            'action': _('域名详情'),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

class DomainNameRecordsListView(AdminUserRequiredMixin, SingleObjectMixin, TemplateView):
    template_name = 'domain_name/records_list.html'
    model = DomainName
    object = None

    def get_context_data(self, **kwargs):
        context = {
            'app': _('域名管理'),
            'action': _('域名解析记录'),
            'object': self.get_object()
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

class DomainNameRecordCreateView(AdminUserRequiredMixin, SuccessMessageMixin, CreateView):
    model = Records
    template_name = 'domain_name/records_create_update.html'
    form_class = DomainNameRecordForm
    success_message = '"<b>%(domain_name)s</b> 添加记录成功。"'
    def get_success_url(self):
        domain_name = self.object.domain_name
        return reverse('domain-name:records-list', kwargs={"pk": domain_name.id})

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        domain_name_id = self.kwargs.get("pk")
        domain_name = get_object_or_none(DomainName, id=domain_name_id)
        if domain_name:
            form['domain_name'].initial = domain_name
        return form

    def form_valid(self, form):
        record = form.save(commit=False)

        add_record = GetDomainName.record_create(record)

        if add_record['code']:
            add_record = add_record['message']
            record.record_id = add_record['RecordId']
            record.save()
        else:
            form.add_error(
                "rr", add_record['message']
            )
            return self.form_invalid(form)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = {
            'app': '域名管理',
            'action': '添加解析记录',
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

class DomainNameRecordUpdateView(AdminUserRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Records
    template_name = 'domain_name/records_create_update.html'
    form_class = DomainNameRecordForm
    success_message = "<b>%(domain_name)s</b> 记录修改成功。"

    def get_success_url(self):
            domain_name = self.object.domain_name
            return reverse('domain-name:records-list', kwargs={"pk": domain_name.id})

    def get_context_data(self, **kwargs):
        context = {
            'app': '域名管理',
            'action': '修改解析记录',
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        record = form.save(commit=False)

        update_record = GetDomainName.record_modify(record)

        if update_record['code']:
            update_record = update_record['message']
            record.record_id = update_record['RecordId']
            record.save()
        else:
            form.add_error(
                "record_id", update_record['message']
            )
            return self.form_invalid(form)
        return super().form_valid(form)