# -*- coding: utf-8 -*-
#
from django import forms

from ..models import Account
from assets.models import Node, AdminUser, Domain

__all__ = ['CreateCHostForm',]

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
    MACHINETYPE_TYPE_CHOICES = (
        ('N', '通用型 N'),
        ('C', '高主频型 C'),
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
        required=True, queryset=Account.objects.filter(auth__contains='chost'),
        label="账号",
        widget=forms.Select(
            attrs={
                'class': 'select2',
                'data-placeholder': '账号'
            }
        )
    )
    ChargeType = forms.ChoiceField(initial='Month', choices=CHARGE_TYPE_CHOICES, required=False, label='计费模式')
    Quantity = forms.IntegerField(label='购买时长')
    Region = forms.CharField(required=True, label='地域')
    Zone = forms.CharField(required=True, label='可用区')
    ProjectId = forms.CharField(required=True, label='项目')
    nodes = forms.ModelMultipleChoiceField(
        queryset=Node.objects.all(), label='节点',
        widget=forms.SelectMultiple(
            attrs={'class': 'select2', 'data-placeholder': '节点'}
        )
    )

    admin_user = forms.ModelChoiceField(
        queryset=AdminUser.objects.all(), label='管理用户',
        widget=forms.Select(
            attrs={'class': 'select2', 'data-placeholder': '管理用户'}
        )
    )
    Domain = forms.ModelChoiceField(
        queryset=Domain.objects.all(), label='网域',
        widget=forms.Select(
            attrs={'class': 'select2', 'data-placeholder': '网域'}
        )
    )
    MachineType = forms.ChoiceField(choices=MACHINETYPE_TYPE_CHOICES,required=True, label='机型',
        widget=forms.Select(
            attrs={
                'class': 'select2',
                'data-placeholder': '机型'
            })
        )
    NetCapability =forms.ChoiceField(initial='Normal', choices=NET_CAPABILITY_CHOICES, required=False, label='网络增强')
    HotplugFeature = forms.BooleanField(initial=True, label='热升级')
    CPU = forms.IntegerField(required=True, label='CPU', min_value=1, max_value=64,
                            help_text = '可选参数：1-64。'
                             )
    Memory = forms.IntegerField(required=True, label='内存', min_value=1024, max_value=262144,
                                  help_text='单位：MB；范围 ：[1024, 262144]。'
                                  )
    Disks0Type = forms.ChoiceField(initial='CLOUD_SSD', choices=DISK0_TYPE_CHOICES, label='系统盘类型')
    Disks0Size = forms.IntegerField(required=True, label='系统盘大小', min_value=20,
                                  help_text='单位GB。'
                                  )
    Disks1Type = forms.ChoiceField(choices=DISK1_TYPE_CHOICES, required=False,label='数据盘类型')
    Disks1Size = forms.IntegerField(label='数据盘大小', required=False, min_value=20,
                                  help_text='单位GB。'
                                  )
    OSType = forms.ChoiceField(choices=OS_TYPE_CHOICES, label='系统类型')
    ImageType = forms.ChoiceField(choices=IMAGE_TYPE_CHOICES, label='镜像类型')
    ImageId = forms.CharField(label='镜像')

    VPCId = forms.CharField(label='所属VPC')
    SubnetId = forms.CharField(label='所属子网')
    EIP = forms.BooleanField(required=False, label='外网弹性IP')
    EIPPayMode = forms.ChoiceField(initial='Bandwidth', choices=EIP_PAY_MODE_CHOICES, required=False, label='计费方式')
    EIPBandwidth = forms.IntegerField(min_value=1, required=False, label='带宽')
    SecurityGroupId = forms.CharField(max_length=50, label='防火墙')
    Name = forms.CharField(max_length=50, label='实例名称')
    Password = forms.CharField(
        widget=forms.PasswordInput, max_length=128,
        required=True, label='密码',help_text='长度8-30'
    )
    SSHPort = forms.IntegerField(initial=1932, label='SSH端口')