# -*- coding: utf-8 -*-
#

import uuid

from django.db import models
from django.utils.translation import ugettext_lazy as _

from common.utils import get_signer

__all__ = ['Account']
signer = get_signer()

class Account(models.Model):
    RESOLVER_CHOICES = (
        ('ucloud', 'UCloud'),
        ('aliyun', '阿里云'),
    )
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(max_length=50, verbose_name='名称')
    access_id = models.CharField(max_length=128, verbose_name='Access Key ID')
    _access_key = models.TextField(verbose_name='Access Key Secret')
    cloud_service_providers = models.CharField(max_length=50, choices=RESOLVER_CHOICES, verbose_name='云服务商')
    comment = models.TextField(max_length=128, default='', blank=True, verbose_name=_('Comment'))

    class Meta:
        verbose_name = "云管账号"
        unique_together = [('name')]
        db_table = "cmis_account"

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
        print(signer.sign(password))
        self._access_key = signer.sign(password)