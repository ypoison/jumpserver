# -*- coding: utf-8 -*-
#

import uuid

from django.db import models
from assets.models import Node, Asset

__all__ = ['PlatformNode', 'NodeConfigRecords']

class PlatformNode(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    platform = models.ForeignKey(Node, on_delete=models.CASCADE, verbose_name='项目')
    public_node = models.ForeignKey(Asset, related_name='public_node_asset', on_delete=models.CASCADE, verbose_name='公共节点')
    public_node_port = models.ImageField(default=10125, verbose_name='公共节点端口')
    private_node = models.ForeignKey(Asset,  related_name='private_node_asset', on_delete=models.CASCADE, verbose_name='私有节点')
    private_node_port = models.ImageField(default=10125, verbose_name='私有节点端口')
    comment = models.TextField(max_length=128, null=True, blank=True, verbose_name='备注')

    def __str__(self):
        return self.platform.name

    class Meta:
        verbose_name = '平台节点'
        db_table = 'config_node_to_platform'

class NodeConfigRecords(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    platfrom = models.ForeignKey(PlatformNode, on_delete=models.CASCADE, verbose_name='平台')
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