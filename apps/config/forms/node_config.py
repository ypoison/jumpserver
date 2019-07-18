# -*- coding: utf-8 -*-
#
from django import forms
from django.shortcuts import get_object_or_404
from assets.models import Node, Asset
from ..models import WEBConfigRecords

__all__ = [ 'WEBConfigForm']

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
    node_asset = forms.CharField(max_length=64,required=True)
    proxy_asset = forms.CharField(max_length=64,required=True)
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super(WEBConfigForm, self).__init__(*args, **kwargs)
        self.fields['platform'].queryset = Node.objects.filter(key__regex=r'^1:[0-9]$|[0-9][0-9]$|[0-9][0-9][0-9]$').exclude(code="GGDLJD")
    class Meta:
        model = WEBConfigRecords
        fields = ['platform', 'node_asset', 'domain', 'port', 'proxy_asset', 'proxy_ip', 'proxy_port','comment']

    def clean_node_asset(self):
        node_asset_id = self.cleaned_data['node_asset']
        node_asset = get_object_or_404(Asset, id=node_asset_id)
        return node_asset

    def clean_proxy_asset(self):
        proxy_asset_id = self.cleaned_data['proxy_asset']
        proxy_asset = get_object_or_404(Asset, id=proxy_asset_id)
        return proxy_asset