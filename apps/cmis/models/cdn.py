# -*- coding: utf-8 -*-
#

import uuid

from django.db import models
from ..models import Account
from common.utils import get_signer

__all__ = ['CDNDomain',]
signer = get_signer()

class CDNDomain(models.Model):
    TYPE_CHOICES = (
        ('web', '图片及小文件分发'),
        ('download', '大文件下载加速'),
        ('video', '视音频点播加速'),
        ('liveStream', '直播流媒体加速'),
    )
    SCOPE_CHOICES = (
        ('domestic', '中国大陆(需备案)'),
        ('overseas', '港澳台及海外(无需备案)'),
        ('global', '全球加速(需备案)'),
        )
    SOURCE_TYPE_CHOICES = (
        ('ipaddr', 'IP源站'),
        ('domain', '域名源站'),
        ('oss', 'OSS Bucket为源站'),
        )
    SOURCE_PORT_CHOICES = (
        (80, '80端口'),
        (443, '443端口'),
        )
    DOMAIN_STATUS_CHOICES = (
        ('online', '启用'),
        ('offline', '停用'),
        ('configuring', '配置中'),
        ('configure_failed', '配置失败'),
        ('checkingring', '正在审核'),
        ('check_failed', '审核失败')
    )
    HTTPS_CHOICES = (
        ('on', 'on'),
        ('off', 'off'),
        )

    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name='所属账号')
    domain_name = models.CharField(max_length=20, verbose_name='域名')
    cname = models.CharField(max_length=128, blank=True, null=True, verbose_name='CNAME域名')
    cdn_type = models.CharField(max_length=20, choices=TYPE_CHOICES,verbose_name='业务类型')
    check_url = models.CharField(max_length=128, blank=True, null=True,  verbose_name='检测url')
    owner_account = models.CharField(max_length=128,  blank=True, null=True, verbose_name='OwnerAccount')
    resource_group_id = models.CharField(max_length=50, blank=True, null=True, verbose_name='资源组ID')
    scope = models.CharField(max_length=10, default='domestic', choices=SCOPE_CHOICES, verbose_name='加速区域')
    source_port = models.IntegerField(default=80, choices=SOURCE_PORT_CHOICES, verbose_name='端口')
    source_type = models.CharField(max_length=10, choices=SOURCE_TYPE_CHOICES, verbose_name='源站类型')
    sources = models.CharField(max_length=128, verbose_name='回源地址')
    domain_status = models.CharField(max_length=20, blank=True, null=True, choices=SOURCE_PORT_CHOICES, verbose_name='资源组ID')
    https = models.CharField(max_length=5,default='off', choices=HTTPS_CHOICES, verbose_name='https')
    gmt_created = models.CharField(max_length=20, choices=HTTPS_CHOICES, blank=True, null=True, verbose_name='创建时间')
    comment = models.TextField(max_length=128, default='', blank=True, verbose_name='备注')

    class Meta:
        unique_together = [('domain_name')]
        verbose_name = "域名"
        db_table = "cmis_cdn_domain"

    def __str__(self):
        return self.domain_name