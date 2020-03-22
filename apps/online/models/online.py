# -*- coding: utf-8 -*-
#

import uuid
from django.shortcuts import get_object_or_404
from django.db import models

from assets.models import Node

__all__ = ['Online', 'LatestOnline']

class Online(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    platform = models.CharField(max_length=20, verbose_name='平台')
    online_num = models.IntegerField(verbose_name='在线数')
    push_num = models.IntegerField(verbose_name='推送次数')
    time = models.DateTimeField(verbose_name='采集时间')
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}{}:{}'.format(self.platform, self.time, self.online_num)

    class Meta:
        verbose_name = '在线人数'
        db_table = 'online_number'

class LatestOnline(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    platform = models.CharField(max_length=20, verbose_name='平台')
    online_num = models.IntegerField(verbose_name='在线数')
    date_updated = models.DateField(auto_now_add=True)

    def __str__(self):
        return '{}:{}'.format(self.platform, self.online_num)

    class Meta:
        verbose_name = '最新在线人数'
        db_table = 'online_latest_number'
        unique_together = [('platform', 'date_updated')]

    @property
    def get_platform_value(self):
        return get_object_or_404(Node, code=self.platform).value