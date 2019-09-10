# -*- coding: utf-8 -*-
#
from django.views.generic import TemplateView, CreateView, \
    UpdateView, FormView

from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse_lazy
from django.shortcuts import redirect

from django.contrib.auth.mixins import LoginRequiredMixin

from ..models import CDNDomain, Account
from ..forms import CDNDomainForm, CDNFreshForm

from ..aliyun import AliyunCDN


__all__ = (
    "CDNDomainListView", "CDNDomainCreateView", "CDNDomainDetailView",
    "CDNFreshCreateView", "CDNFreshListView",
)
SetCDN = AliyunCDN()

class CDNDomainListView(LoginRequiredMixin, TemplateView):
    template_name = 'cmis/cdn_list.html'

    def get_context_data(self, **kwargs):
        context = {
            'app': _('云管中心'),
            'action': _('CDN列表'),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

class CDNDomainCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = CDNDomain
    template_name = 'cmis/cdn_create.html'
    form_class = CDNDomainForm
    success_url = reverse_lazy('cmis:cdn-list')
    success_message = "<b>%(domain_name)s</b> was updated successfully."

    def form_valid(self, form):
        domain = form.save(commit=False)
        kw = domain.__dict__
        kw['access_id'] = domain.account.access_id
        kw['access_key'] = domain.account.access_key
        add_domain = SetCDN.cdn_create(**kw)

        if add_domain['code']:
            domain.save()
        else:
            form.add_error(
                "domain_name", add_domain['msg']
            )
            return self.form_invalid(form)
        return super().form_valid(form)


    def get_context_data(self, **kwargs):
        context = {
            'app': '云管中心',
            'action': '添加CDN',
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

class CDNDomainDetailView(LoginRequiredMixin, UpdateView):
    model = CDNDomain
    context_object_name = 'cdn'
    template_name = 'cmis/cdn_detail.html'
    form_class = CDNDomainForm

    def get_context_data(self, **kwargs):
        context = {
            'app': '云管中心',
            'action': 'CDN详情',
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

class CDNFreshListView(LoginRequiredMixin, TemplateView):
    template_name = 'cmis/cdn_fresh_list.html'

    def get_context_data(self, **kwargs):
        context = {
            'app': '云管中心',
            'action': '刷新预热',
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

class CDNFreshCreateView(LoginRequiredMixin, SuccessMessageMixin, FormView):
    template_name = 'cmis/cdn_fresh_create.html'
    form_class = CDNFreshForm
    success_url = reverse_lazy('cmis:cdn-fresh-list')
    success_message = "操作成功。"

    def get_context_data(self, **kwargs):
        context = {
            'app': '云管中心',
            'action': '刷新预热',
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        req = request.POST
        account_id = req.get('account')
        ObjectPath = req.get('object_path')
        action = req.get('action')
        object_type = req.get('object_type')
        try:
            account = Account.objects.get(id=account_id)
        except Exception as e:
            return redirect(reverse_lazy('cmis:cdn-fresh-create'))
        kw = {
            'access_id': account.access_id,
            'access_key': account.access_key,
            'action': action,
            'ObjectPath': ObjectPath,
            'ObjectType': object_type

        }
        fresh = SetCDN.fresh_set(**kw)
        if not fresh['code']:
            self.success_message = fresh['msg']
            return redirect(reverse_lazy('cmis:cdn-fresh-create'))
        return redirect(self.success_url)