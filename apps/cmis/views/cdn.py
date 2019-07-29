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
from ..models import CDNDomain
from ..forms import CDNDomainForm

from ..aliyun import AliyunCDN


__all__ = (
    "CDNDomainListView", "CDNDomainCreateView", "CDNDomainDetailView",
)
SetCDN = AliyunCDN()

class CDNDomainListView(AdminUserRequiredMixin, TemplateView):
    template_name = 'cmis/cdn_list.html'

    def get_context_data(self, **kwargs):
        context = {
            'app': _('云管中心'),
            'action': _('CDN列表'),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

class CDNDomainCreateView(AdminUserRequiredMixin, SuccessMessageMixin, CreateView):
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
                "domain_name", add_domain['message']
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

class CDNDomainDetailView(AdminUserRequiredMixin, DetailView):
    model = CDNDomain
    context_object_name = 'cdn'
    template_name = 'cmis/cdn_detail.html'

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Assets'),
            'action': _('Asset detail'),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)