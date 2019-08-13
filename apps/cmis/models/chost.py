# -*- coding: utf-8 -*-
#

import uuid

from django.db import models
from assets.models import Asset
from ..models import Account
from common.utils import get_signer, get_object_or_none

__all__ = ['ChostCreateRecord',]
signer = get_signer()

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