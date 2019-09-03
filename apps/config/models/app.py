# -*- coding: utf-8 -*-
#

import uuid

from django.db import models

__all__ = ['App']

class App(models.Model):
    TYPE_CHOICES = (
        ('game', '游戏服'),
        ('other', '其它'),
    )
    name = models.CharField(max_length=50, verbose_name='名称')
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, verbose_name='类型')
    port = models.IntegerField(verbose_name='端口')

    class Meta:
        unique_together = [('name')]
        db_table = "config_app"