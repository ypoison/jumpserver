# -*- coding: utf-8 -*-
#
from django import forms
from orgs.mixins import OrgModelForm
from ..models import DomainName, Records, Account

__all__ = ['DomainNameForm','DomainNameRecordForm', 'DomainNameAccountForm']

class DomainNameAccountForm(forms.ModelForm):
    access_key = forms.CharField(
        widget=forms.PasswordInput, max_length=128,
        strip=True
    )

    def save(self, commit=True):
        access_key = self.cleaned_data.get('access_key')
        account = super().save(commit=commit)
        if access_key:
            account.access_key = access_key
            account.save()
        return account

    class Meta:
        model = Account
        fields = ['name', 'access_id', 'access_key', 'resolver', 'comment']

class DomainNameForm(OrgModelForm):
    class Meta:
        model = DomainName
        fields = ['account', 'domain_name', 'project', 'registrar', 'registration_date', 'expiration_date', 'dns_high_anti', 'beian', 'ch_lose', 'comment']
        help_texts = {
            'registration_date':'例:2021-06-02 12:12:12',
            'expiration_date':'例:2021-06-02 12:12:12',
            'dns_high_anti': '高防厂家名称,没有高防不用填。',
            #ch_lose': '被墙填0，没被墙填1。'
        }

class DomainNameRecordForm(OrgModelForm):
    class Meta:
        model = Records
        fields = ['domain_name', 'type','rr','line','value','priority','ttl', 'comment']