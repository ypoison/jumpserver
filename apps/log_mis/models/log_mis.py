# -*- coding: utf-8 -*-
#

import uuid

from django.db import models
from django.shortcuts import get_object_or_404

from assets.models import Asset

__all__ = ['Records', 'RecordsTree']

class Records(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    platform = models.CharField(max_length=20, verbose_name='平台')
    name = models.CharField(max_length=50,verbose_name='名称')
    path = models.CharField(max_length=128,verbose_name='路径')
    md5 = models.CharField(max_length=128,verbose_name='MD5')
    size = models.CharField(max_length=10,verbose_name='大小')
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}{}'.format(self.path, self.name)

    class Meta:
        verbose_name = '日志记录'
        db_table = 'log_records'
        unique_together = [('platform','path','name')]

class RecordsTree(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    key = models.CharField(unique=True, max_length=128, verbose_name="Key")  # 'king/api_log/api_gateway'
    value = models.CharField(max_length=128, verbose_name="值")
    date_create = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '日志记录树'
        db_table = 'log_records_tree'

    @classmethod
    def get_tree_root(cls):
        root = cls.objects.filter(key__regex=r'^[A-Za-z0-9_-]+/$')
        if root:
            return root

    def as_tree_node(self, is_root):
        from ..serializers import RecordsTreeSerializer
        from common.tree import TreeNode
        from common.utils import get_object_or_none
        node_serializer = RecordsTreeSerializer(instance=self)
        data = {
            'id': self.key,
            'name': self.value,
            'isParent': True,
            'open': is_root,
            'meta': {
                'node': node_serializer.data,
                'type': 'node'
            }
        }
        tree_node = TreeNode(**data)
        return tree_node

    def get_children(self):
        pattern = r'^{0}[A-Za-z0-9_-]+/$'
        return self.__class__.objects.filter(
            key__regex=pattern.format(self.key)
        )

    def get_asset(self):
        platform = self.key.split('/')[0]
        log_asset = get_object_or_404(Asset, hostname='{}-Backup'.format(platform))
        return log_asset