# -*- coding: utf-8 -*-
#
from django import forms

from ..models import Account
from assets.models import Node

__all__ = ['AccountForm']

class AccountForm(forms.ModelForm):
    AUTH_CHOICES = (
        ('chost', '云主机'),
        ('cdn', 'CDN'),
    )
    access_key = forms.CharField(
        widget=forms.PasswordInput, max_length=128,
        strip=True
    )

    auth = forms.MultipleChoiceField(
        label='操作权限', choices=AUTH_CHOICES,
        widget=forms.SelectMultiple(
            attrs={'class': 'select2', 'data-placeholder': '操作权限'}
        )
    )

    class Meta:
        model = Account
        fields = ['name', 'auth', 'access_id', 'access_key', 'cloud_service_providers', 'comment']

    def __init__(self, *args, **kwargs):
        if kwargs.get('instance', None):
            initial = kwargs.get('initial', {})
            initial['auth'] = kwargs['instance'].auth_list
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        access_key = self.cleaned_data.get('access_key')
        account = super().save(commit=commit)
        if access_key:
            account.access_key = access_key
            account.save()
        return account