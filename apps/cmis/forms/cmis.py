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
    NET_CAPABILITY_CHOICES = (
        ('Normal', '不开启'),
        ('Super', '网络增强1.0'),
        ('Ultra', '网络增强2.0'),
    )
    EIP_PAY_MODE_CHOICES = (
        ('Traffic', '流量计费'),
        ('Bandwidth', '带宽计费'),
        ('ShareBandwidth', '共享带宽模式'),
        ('Free', '免费带宽模式'),
    )
    HOST_TYPE_CHOICES = (
        ('N3', '标准型 N3'),
        ('C1', '高主频型 C1'),
        ('N2', '标准型 N2'),
        ('I2', '高IO型 I2'),
        ('G2', 'GPU型 - P40'),
        ('G3', 'GPU型 - V100'),
    )
    DISK0_TYPE_CHOICES = (
        ('LOCAL_NORMAL', '普通本地盘'),
        ('LOCAL_SSD', 'SSD本地盘'),
        ('CLOUD_SSD', 'SSD云盘'),
    )
    DISK1_TYPE_CHOICES =  (
        ('', '---------'),
        ('LOCAL_NORMAL', '普通本地盘'),
        ('LOCAL_SSD', 'SSD本地盘'),
        ('CLOUD_SSD', 'SSD云盘'),
        ('CLOUD_NORMAL', '普通云盘'),
        ('CLOUD_RSSD', 'RSSD云盘'),
        ('EXCLUSIVE_LOCAL_DISK', '独享本地盘'),
    )
    IMAGE_TYPE_CHOICES = (
        ('', '---------'),
        ('Base', '标准镜像'),
        ('Custom', '自定义镜像'),
        ('Business', '行业镜像'),
    )
    OS_TYPE_CHOICES = (
        ('Linux', 'Linux'),
        ('Windows', 'Windows'),
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
    region = forms.ChoiceField(required=True, label='地域')
    zone = forms.ChoiceField(required=True, label='可用区')
    project = forms.ChoiceField(required=True, label='项目')

    host_type = forms.ChoiceField(choices=HOST_TYPE_CHOICES,required=True, label='机型',
        widget=forms.Select(
            attrs={
                'class': 'select2',
                'data-placeholder': '机型'
            })
        )
    net_capability =forms.ChoiceField(initial='Normal', choices=NET_CAPABILITY_CHOICES, required=False, label='网络增强')
    cpu = forms.IntegerField(required=True, label='CPU',
                            help_text = '可选参数：1-64。'
                             )
    memory = forms.IntegerField(required=True, label='内存',
                                  help_text='单位：MB；范围 ：[1024, 262144]。'
                                  )
    disks0_type = forms.ChoiceField(initial='CLOUD_SSD', choices=DISK0_TYPE_CHOICES, label='系统盘类型')
    disks0_size = forms.IntegerField(required=True, label='系统盘大小',
                                  help_text='单位GB。'
                                  )
    disks1_type = forms.ChoiceField(choices=DISK1_TYPE_CHOICES, required=False,label='数据盘类型')
    disks1_size = forms.IntegerField(label='数据盘大小',required=False,
                                  help_text='单位GB。'
                                  )
    os_type = forms.ChoiceField(choices=OS_TYPE_CHOICES, label='系统类型')
    image_type = forms.ChoiceField(choices=IMAGE_TYPE_CHOICES, label='镜像类型')
    image = forms.ChoiceField(label='镜像')

    vpc = forms.ChoiceField(label='所属VPC')
    subnet = forms.ChoiceField(label='所属子网')
    eip = forms.BooleanField(required=False, label='外网弹性IP')
    eip_pay_mode = forms.ChoiceField(initial='Bandwidth', choices=EIP_PAY_MODE_CHOICES, required=False, label='计费方式')
    eip_bandwidth = forms.IntegerField(required=False, label='带宽')
    name = forms.CharField(max_length=50, label='实例名称')
    passwd = forms.CharField(
        widget=forms.PasswordInput, max_length=128,
        required=True, label='密码'
    )