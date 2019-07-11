# -*- coding: utf-8 -*-
#
from django import forms
from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404
from django.db import models
from orgs.mixins import OrgModelForm
from assets.models import Node, Asset
from ..models import WEBConfigRecords

__all__ = ['PlatformNodeConfigForm', 'WEBConfigForm']

class PlatformNodeConfigForm(forms.ModelForm):
    platform = forms.ModelChoiceField(
        required=True, queryset=Node.objects.filter(code=1),
        label="平台",
        widget=forms.Select(
            attrs={
                'class': 'select2',
                'data-placeholder': '平台'
            }
        )
    )
    public_node_asset = forms.ModelChoiceField(
        queryset=Asset.objects.filter(port=1), label='公共节点', required=True,
        widget=forms.Select(
            attrs={'class': 'select2', 'data-placeholder': _('Select assets')}
        )
    )
    private_node_asset = forms.CharField(max_length=64,required=True)
    class Meta:
        model = Node
        fields = ['platform', 'public_node_asset', 'private_node_asset']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super(PlatformNodeConfigForm, self).__init__(*args, **kwargs)
        self.fields['platform'].queryset = Node.objects.filter(key__regex=r'^1:[0-9]$').exclude(code="GGDLJD")
        self.fields['public_node_asset'].queryset = Node.objects.get(code="GGDLJD").get_all_assets()

    def clean_private_node_asset(self):
        private_node_asset_id = self.cleaned_data['private_node_asset']
        private_node_asset = get_object_or_404(Asset, id=private_node_asset_id)
        return private_node_asset

    def save(self, commit=True):
        platform = self.cleaned_data.get('platform')
        public_node_asset = self.cleaned_data.get('public_node_asset')
        private_node_asset = self.cleaned_data.get('private_node_asset')
        platform.public_node_asset = public_node_asset
        platform.private_node_asset = private_node_asset
        platform.save()
        return platform

class WEBConfigForm(forms.ModelForm):
    platform = forms.ModelChoiceField(
        required=True, queryset=Node.objects.filter(code=1),
        label="平台",
        widget=forms.Select(
            attrs={
                'class': 'select2',
                'data-placeholder': '平台'
            }
        )
    )
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super(WEBConfigForm, self).__init__(*args, **kwargs)
        self.fields['platform'].queryset = Node.objects.filter(key__regex=r'^1:[0-9]$').exclude(code="GGDLJD").exclude(public_node_asset__isnull=True)
    class Meta:
        model = WEBConfigRecords
        fields = ['platform', 'domain', 'port', 'proxy_ip', 'proxy_port','comment']