# -*- coding: utf-8 -*-
#
from django import forms
from orgs.mixins import OrgModelForm
from ..models import DomainName, Records, Account

import re

__all__ = ['DomainNameForm','DomainNameRecordForm', 'DomainNameAccountForm']


def is_domain(domain):
    domain_regex = re.compile(
        r'(?:[A-Z0-9_](?:[A-Z0-9-_]{0,247}[A-Z0-9])?\.)+(?:[A-Z]{2,6}|[A-Z0-9-]{2,}(?<!-))\Z',
        re.IGNORECASE)
    return True if domain_regex.match(domain) else False


def is_ipv4(address):
    ipv4_regex = re.compile(
        r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$",
        re.IGNORECASE)
    return True if ipv4_regex.match(address) else False


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
        fields = ['domain_name', 'type', 'rr', 'line', 'value', 'priority', 'ttl', 'comment']

    def clean_value(self):
        type = self.cleaned_data['type']
        value = self.cleaned_data['value']
        if type == 'A':
            check = is_ipv4(value)
            print(check)
            if not check:
                msg = 'A记录的记录值为IP形式(如10.11.12.13)'
                raise forms.ValidationError(msg)
        elif type == 'CNAME':
            check = is_domain(value)
            if not check:
                msg = 'CNAME记录的记录值为域名形式(如abc.example.com)'
                raise forms.ValidationError(msg)
        return value