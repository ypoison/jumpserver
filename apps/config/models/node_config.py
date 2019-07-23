# -*- coding: utf-8 -*-
#

import uuid

from django.db import models
from assets.models import Node, Asset

__all__ = ['WEBConfigRecords']

class WEBConfigRecords(models.Model):
    PORT_CHOICES = (
        (8890, 'honghei(8890)'),
        (8893, 'qznn(8893)'),
        (8894, 'brnn(8894)'),
        (8895, 'bjl(8895)'),
        (8896, 'ttz(8896)'),
        (8897, 'zhajinhua(8897)'),
        (8898, 'lhd(8898)'),
        (8899, 'shaibao(8899)'),
        (8900, 'redpacket(8900)'),
        (8901, 'paigow(8901)'),
        (8902, 'sumkung(8902)'),
        (8903, 'benzbmw(8903)'),
        (8033, 'pay(8033)'),
        (8049, 'h5(8049)'),
    )
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    platform = models.ForeignKey(Node, on_delete=models.CASCADE, verbose_name='平台')
    node_asset = models.ForeignKey(Asset,null=True, related_name='node_asset', on_delete=models.SET_NULL, verbose_name='节点主机')
    domain =models.CharField(max_length=128, verbose_name='域名')
    port = models.IntegerField(choices=PORT_CHOICES, verbose_name='端口')
    proxy_asset = models.ForeignKey(Asset,null=True, related_name='proxy_asset', on_delete=models.SET_NULL, verbose_name='代理主机')
    proxy_ip = models.GenericIPAddressField(max_length=32, verbose_name='代理IP')
    proxy_port = models.IntegerField(choices=PORT_CHOICES, verbose_name='代理端口')
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