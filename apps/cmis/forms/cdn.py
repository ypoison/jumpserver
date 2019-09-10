# -*- coding: utf-8 -*-
#
from django import forms
from ..models import CDNDomain, Account

__all__ = ['CDNDomainForm','CDNFreshForm']

class CDNDomainForm(forms.ModelForm):
    account = forms.ModelChoiceField(
        required=True, queryset=Account.objects.filter(auth__contains='cdn'),
        label="账号",
        widget=forms.Select(
            attrs={
                'class': 'select2',
                'data-placeholder': '账号'
            }
        )
    )
    class Meta:
        model = CDNDomain
        fields = ['account', 'domain_name', 'cdn_type', 'check_url', 'owner_account',
                  'resource_group_id', 'scope', 'source_port', 'source_type',
                  'sources', 'comment']
        widgets = {
            'sources': forms.TextInput(attrs={'placeholder': '1.1.1.1:20,2.1.1.1:30'}),
        }
        help_texts = {
            'sources':'20为主，30为备；如：1.1.1.1:20,2.1.1.1:30；source1.dymis.com:20,source2.dymis.com:30',
        }

class CDNFreshForm(forms.Form):
    ACTION_CHOICES = (
        ('RefreshCaches', '刷新'),
        ('PushCache', '预热'),
    )
    OBJECT_TYPE_CHOICES = (
        ('File', 'URL'),
        ('Directory', '目录'),
        )
    account = forms.ModelChoiceField(
        required=True, queryset=Account.objects.filter(auth__contains='cdn'),
        label="账号",
        widget=forms.Select(
            attrs={
                'class': 'select2',
                'data-placeholder': '账号'
            }
        )
    )
    action = forms.ChoiceField(choices=ACTION_CHOICES, label='操作类型')
    object_type = forms.ChoiceField(initial='File', choices=OBJECT_TYPE_CHOICES, label='源站类型')
    object_path = forms.CharField(label='URL', widget=forms.Textarea,
                                  help_text='目录刷新需以"/"结尾, 如: img.dy.com/dir/',
                                  )