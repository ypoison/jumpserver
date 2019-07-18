# -*- coding: utf-8 -*-
#

import uuid

from django.db import models
from assets.models import Node, Asset

__all__ = ['WEBConfigRecords']

class WEBConfigRecords(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    platform = models.ForeignKey(Node, on_delete=models.CASCADE, verbose_name='平台')
    node_asset = models.ForeignKey(Asset,null=True, related_name='node_asset', on_delete=models.SET_NULL, verbose_name='节点主机')
    domain =models.CharField(max_length=128, verbose_name='域名')
    port = models.IntegerField(verbose_name='端口')
    proxy_asset = models.ForeignKey(Asset,null=True, related_name='proxy_asset', on_delete=models.SET_NULL, verbose_name='代理主机')
    proxy_ip = models.GenericIPAddressField(max_length=32, verbose_name='代理IP')
    proxy_port = models.IntegerField(verbose_name='代理端口')
    comment = models.TextField(max_length=60, null=True, blank=True, verbose_name='备注')


    def __str__(self):
        return self.domain

    class Meta:
        verbose_name = '节点配置'
        db_table = 'config_web_config_records'

    @property
    def platform_display(self):
        return str(self.platform)

    @property
    def node_asset_display(self):
        return str(self.node_asset)

    @property
    def proxy_asset_display(self):
        return str(self.proxy_asset)