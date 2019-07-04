# -*- coding: utf-8 -*-
#
from django import forms
from django.utils.translation import gettext_lazy as _
from django.db import models
from orgs.mixins import OrgModelForm
from assets.models import Node, Asset

__all__ = ['PlatformNodeConfigForm', ]

class PlatformNodeConfigForm(forms.ModelForm):
    platform = forms.ModelChoiceField(
        required=False, queryset=Node.objects.filter(code=1),
        label="平台",
        widget=forms.Select(
            attrs={
                'class': 'select2',
                'data-placeholder': '平台'
            }
        )
    )
    public_node_asset = forms.ModelChoiceField(
        queryset=Node.objects.filter(code=1), label='公共节点', required=False,
        widget=forms.Select(
            attrs={'class': 'select2', 'data-placeholder': _('Select assets')}
        )
    )
    private_node_asset = forms.ModelChoiceField(
        queryset=Node.objects.filter(code=1), label='私有节点', required=False,
        widget=forms.Select(
            attrs={'class': 'select2', 'data-placeholder': _('Select assets')}
        )
    )
    class Meta:
        model = Node
        fields = ['platform', 'public_node_asset', 'private_node_asset']

    def __init__(self, *args, **kwargs):
        super(PlatformNodeConfigForm, self).__init__(*args, **kwargs)
        self.fields['platform'].queryset = Node.objects.filter(key__regex=r'^1:[0-9]$').exclude(code="GGDLJD")
        self.fields['public_node_asset'].queryset = Node.objects.get(code="GGDLJD").get_all_assets()

    def save(self, commit=True):
        instance = super().save(commit=commit)
        assets = self.cleaned_data['assets']
        instance.assets.set(assets)
        return instance
