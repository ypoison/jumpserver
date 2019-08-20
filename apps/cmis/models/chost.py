# -*- coding: utf-8 -*-
#

import uuid

from django.db import models
from assets.models import Asset
from ..models import Account
from common.utils import get_object_or_none

__all__ = ['ChostCreateRecord', 'ChostModel']

class ChostModel(models.Model):
    name = models.CharField(max_length=50, verbose_name='名称')
    charge_type = models.CharField(max_length=10, verbose_name='计费模式')
    quantity = models.IntegerField(verbose_name='购买时长')
    machine_type = models.CharField(max_length=2, verbose_name='机型')
    net_capability = models.CharField(max_length=10, null=True, verbose_name='网络增强')
    cpu = models.IntegerField(verbose_name='CPU')
    memory = models.IntegerField(verbose_name='内存')
    hotplug_feature = models.BooleanField(default=False, verbose_name='热升级')
    disks_0_type = models.CharField(max_length=20, verbose_name='系统盘类型')
    disks_0_size = models.IntegerField(verbose_name='系统盘大小')
    disks_1_type = models.CharField(max_length=20, null=True, verbose_name='数据盘类型')
    disks_1_size = models.IntegerField(null=True, verbose_name='数据盘大小')
    eip = models.BooleanField(default=False, verbose_name='外网弹性IP')
    eip_pay_mode = models.CharField(max_length=15, verbose_name='计费方式')
    eip_bandwidth = models.IntegerField(verbose_name='带宽')
    ssh_port = models.IntegerField(verbose_name='SSH端口')
    region = models.CharField(max_length=50, verbose_name='地域')
    zone = models.CharField(max_length=50, verbose_name='可用区')
    vpc = models.CharField(max_length=50, verbose_name='VPC')
    subnet = models.CharField(max_length=50, verbose_name='子网')
    security_group = models.CharField(max_length=50, verbose_name='防火墙')
    os_type = models.CharField(max_length=20, verbose_name='系统类型')
    image_type = models.CharField(max_length=20, verbose_name='镜像类型')
    image = models.CharField(max_length=20, verbose_name='镜像')


    class Meta:
        unique_together = [('name')]
        verbose_name = "云主机采购模板"
        db_table = "cmis_chost_model"

    def __str__(self):
        return self.name

class ChostCreateRecord(models.Model):
    STATUS_CHOICES = (
        ('Initializing', '初始化'),
        ('Starting', '启动中'),
        ('Running', '运行中'),
        ('Stopping', '关机中'),
        ('Stopped', '关机'),
        ('Install Fail', '安装失败'),
        ('Rebooting', '重启中'),
        ('Error', '创建失败'),
    )
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    account_id = models.CharField(max_length=36, null=True, verbose_name='所属账号')
    region = models.CharField(max_length=20, null=True, verbose_name='地域')
    hid = models.CharField(max_length=50, null=True, verbose_name='云主机ID')
    asset = models.ForeignKey(Asset, on_delete=models.SET_NULL, null=True, verbose_name='资产信息')
    created_by = models.CharField(max_length=32, null=True, blank=True, verbose_name='创建人')
    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name='创建时间')
    status = models.CharField(max_length=128, choices=STATUS_CHOICES, default='', blank=True, verbose_name='状态')

    class Meta:
        verbose_name = "云主机采购记录"
        db_table = "cmis_chost_create_record"

    @property
    def account(self):
        return get_object_or_none(Account, id=uuid.UUID(self.account_id).hex)