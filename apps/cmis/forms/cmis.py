# -*- coding: utf-8 -*-
#
from django import forms

from ..models import Account

__all__ = ['AccountForm', 'CreateCHostForm']

class AccountForm(forms.ModelForm):
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
        fields = ['name', 'access_id', 'access_key', 'cloud_service_providers', 'comment']

class CreateCHostForm(forms.Form):
    CHARGE_TYPE_CHOICES = (
        ('Year', '按年付费'),
        ('Month', '按月付费'),
        ('Dynamic', '按小时付费'),
    )
    account = forms.ModelChoiceField(
        required=True, queryset=Account.objects.all(),
        label="账号",
        widget=forms.Select(
            attrs={
                'class': 'select2',
                'data-placeholder': '账号'
            }
        )
    )
    charge_type = forms.ChoiceField(initial='Month', choices=CHARGE_TYPE_CHOICES, required=False, label='计费模式')
    region = forms.CharField(max_length=50, required=True, label='地域')
    zone = forms.CharField(max_length=50, required=True, label='可用区')
    project = forms.CharField(max_length=50, required=False, label='项目')
    images = forms.CharField(max_length=50, required=True, label='镜像')
    name = forms.CharField(max_length=50, label='实例名称')
    passwd = forms.CharField(
        widget=forms.PasswordInput, max_length=128,
        required=True, label='密码'
    )
    cpu = forms.IntegerField(required=True, label='CPU',
                            help_text = '可选参数：1-64。'
                             )
    memory = forms.IntegerField(required=True, label='内存',
                                  help_text='单位：MB；范围 ：[1024, 262144]。'
                                  )
    disks0_type = forms.CharField(max_length=50, required=True, label='系统盘类型')
    disks0_size = forms.IntegerField(required=True, label='系统盘大小',
                                  help_text='单位GB。'
                                  )
    disks1_type = forms.CharField(max_length=50, required=False, label='数据盘类型')
    disks1_size = forms.IntegerField(label='数据盘大小',required=False,
                                  help_text='单位GB。'
                                  )
    VPC = forms.CharField(max_length=50, required=False, label='所属VPC')
    Subnet = forms.CharField(max_length=50, required=False, label='所属子网')