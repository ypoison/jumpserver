# -*- coding: utf-8 -*-
#

import uuid

from django.db import models
from assets.models import Node, Asset

__all__ = ['NodeConfigRecords']

class NodeConfigRecords(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    platfrom = models.ForeignKey(Node, on_delete=models.CASCADE, verbose_name='平台')
    domain =models.CharField(max_length=128, verbose_name='域名')
    port = models.IntegerField(verbose_name='端口')
    proxy_ip = models.ForeignKey(Asset, on_delete=models.CASCADE, verbose_name='代理IP')
    proxy_port = models.IntegerField(verbose_name='代理端口')
    comment = models.TextField(max_length=128, null=True, blank=True, verbose_name='备注')

    def __init__(self):
        return self.domain

    class Meta:
        verbose_name = '节点配置记录'
        db_table = 'config_node_records'