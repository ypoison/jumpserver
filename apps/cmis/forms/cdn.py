# -*- coding: utf-8 -*-
#
from django import forms
from orgs.mixins import OrgModelForm
from ..models import CDNDomain

__all__ = ['CDNDomainForm']

class CDNDomainForm(forms.ModelForm):
    class Meta:
        model = CDNDomain
        fields = ['account', 'domain_name', 'cdn_type', 'check_url', 'owner_account',
                  'resource_group_id', 'scope', 'source_port', 'source_type',
                  'sources', 'comment']
        help_texts = {
            'sources':'可以是IP或域名。IP支持最多20个，以逗号区分; 域名只能输入一个，IP与域名不能同时输入。',
        }
