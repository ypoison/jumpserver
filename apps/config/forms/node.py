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
        queryset=Asset.objects.filter(port=1), label='公共节点', required=False,
        widget=forms.Select(
            attrs={'class': 'select2', 'data-placeholder': _('Select assets')}
        )
    )
    private_node_asset = forms.ModelChoiceField(
        queryset=Asset.objects.filter(port=1), label='私有节点', required=False,
        widget=forms.Select(
            attrs={'class': 'select2', 'data-placeholder': _('Select assets')}
        )
    )
    class Meta:
        model = Node
        fields = ['platform', 'public_node_asset', 'private_node_asset']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super(PlatformNodeConfigForm, self).__init__(*args, **kwargs)
        self.fields['platform'].queryset = Node.objects.filter(key__regex=r'^1:[0-9]$').exclude(code="GGDLJD")
        self.fields['public_node_asset'].queryset = Node.objects.get(code="GGDLJD").get_all_assets()

    def clean(self):
        super().clean()
        #print(self)
    #    private_node_asset = Asset.objects.get(id=self.request.POST.get('private_node_asset'))
    #    self.cleaned_data['private_node_asset'] = private_node_asset
        print(self.cleaned_data)
    #    return self.cleaned_data

    #def clean_private_node_asset(self):
    #    private = self.cleaned_data['private_node_asset']
    #    print(private)
    #    if private:
    #        return private

    def save(self, commit=True):
        print(1111111111)
        #changed_fields = []
        #for field in self._meta.fields:
        #    if self.data.get(field) not in [None, '']:
        #        changed_fields.append(field)
#
        #cleaned_data = {k: v for k, v in self.cleaned_data.items()
        #                if k in changed_fields}
        #node_id = cleaned_data.pop('id')
        #print(node_id)
        #public = cleaned_data.pop('public_node_asset')
        #print(public)
        #private = cleaned_data.pop('private_node_asset')
        #print(private)
        #assets = Asset.objects.filter(id__in=[asset.id for asset in assets])
        #assets.update(**cleaned_data)
#
        #return assets
