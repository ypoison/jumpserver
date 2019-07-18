# -*- coding: utf-8 -*-
#

import uuid

from django.db import models
from django.utils.translation import ugettext_lazy as _
from orgs.mixins import OrgModelMixin

from common.utils import get_signer

__all__ = ['DomainName', 'Records', 'Account']
signer = get_signer()

class Account(OrgModelMixin):
    RESOLVER_CHOICES = (
        ('aliyun', '阿里云'),
        ('dnspod', 'DNSPod'),
    )
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(max_length=50, verbose_name='名称')
    access_id = models.CharField(max_length=50, verbose_name='账号')
    _access_key = models.CharField(max_length=128,verbose_name='key')
    resolver = models.CharField(max_length=50, choices=RESOLVER_CHOICES, verbose_name='所属域名解析商')
    comment = models.TextField(max_length=128, default='', blank=True, verbose_name=_('Comment'))
    
    class Meta:
        verbose_name = "域名管理账号"
        unique_together = [('name')]
        db_table = "domain_name_account"

    def __str__(self):
        return self.name
        #return '%s.%s' % (self.name, self.resolver)

    @property
    def access_key(self):
        password = signer.unsign(self._access_key)
        if password:
            return password
        else:
            return ""

    @access_key.setter
    def access_key(self, password):
        self._access_key = signer.sign(password)

class DomainName(OrgModelMixin):
    BEIAN_CHOICES = (
        (0, '掉备案'),
        (1, '正常'),
        (2, '未备案'),
    )
    GFW_CHOICES = (
        (0, '被墙'),
        (1, '正常'),
        )
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name='所属账号')
    domain_name = models.CharField(max_length=20, verbose_name='域名')
    project = models.CharField(max_length=20, blank=True, null=True, verbose_name='所属项目')
    registrar = models.CharField(max_length=50, blank=True, null=True, verbose_name='域名注册商')
    registration_date = models.CharField(max_length=20, blank=True, null=True, verbose_name='注册时间')
    expiration_date = models.CharField(max_length=20, blank=True, null=True, verbose_name='到期时间')
    domain_status = models.IntegerField(default=3,verbose_name='状态')
    beian = models.IntegerField(blank=True, null=True, choices=BEIAN_CHOICES, verbose_name='备案状态')
    dns_high_anti = models.CharField(max_length=50, blank=True, null=True, verbose_name='高防')
    ch_lose = models.IntegerField(default=1, choices=GFW_CHOICES, blank=True, null=True, verbose_name='被墙')
    comment = models.TextField(max_length=128, default='', blank=True, verbose_name=_('Comment'))

    class Meta:
        unique_together = [('domain_name')]
        verbose_name = "域名"
        db_table = "domain_name"

    def __str__(self):
        return self.domain_name

class Records(OrgModelMixin):
    TYPE_CHOICES = (
        ('A', 'A'),
        ('CNAME', 'CNAME'),
        ('AAAA', 'AAAA'),
        ('NS', 'NS'),
        ('MX', 'MX'),
        ('SRV', 'SRV'),
        ('TXT', 'TXT'),
        ('CAA', 'CAA'),
        ('REDIRECT_URL', '显性URL'),
        ('FORWARD_URL', '隐性URL'),
    )

    LINE_CHOICES = (
        ('default', '默认'),
        ('telecom', '电信'),
        ('unicom', '联通'),
        ('mobile', '移动'),
        ('oversea', '海外'),
        ('edu', '教育网'),
        ('drpeng', '鹏博士'),
        ('btvn', '广电网'),
    )

    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    record_id = models.CharField(max_length=50, verbose_name='记录ID')
    domain_name = models.ForeignKey(DomainName, on_delete=models.CASCADE, verbose_name='域名')
    type = models.CharField(max_length=15, choices=TYPE_CHOICES, verbose_name='记录类型')
    rr = models.CharField(max_length=50, verbose_name='主机记录')
    line = models.CharField(max_length=25, default='default', choices=LINE_CHOICES, verbose_name='解析线路')
    value = models.CharField(max_length=512, verbose_name='记录值')
    priority = models.IntegerField(blank=True, null=True, verbose_name='MX优先级')
    ttl = models.IntegerField(default=600, verbose_name='TTL')
    status = models.CharField(default='ENABLE', max_length=10, verbose_name='状态')
    locked = models.CharField(max_length=10, blank=True, null=True, verbose_name='锁定状态')
    comment = models.TextField(max_length=128, default='', blank=True, verbose_name=_('Comment'))

    class Meta:
        verbose_name = "域名记录"
        db_table = "domain_name_records"

    def __str__(self):
        return '%s.%s' % (self.rr, self.domain_name)