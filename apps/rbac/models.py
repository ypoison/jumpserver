# -*- coding: utf-8 -*-
#

import uuid

from django.db import models

from users.models import UserGroup, User

class Menu(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(max_length=10,verbose_name='名称')
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True,blank=True, verbose_name='上级菜单')
    icon = models.CharField(max_length=30,null=True,blank=True,verbose_name='小图标')
    html_class = models.CharField(max_length=200,null=True,blank=True,verbose_name='样式')
    url = models.CharField(max_length=200, verbose_name='链接')
    assist_url = models.TextField(null=True,blank=True,verbose_name='辅助链接')
    key = models.CharField(max_length=128, verbose_name='键')
    child_mark = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "菜单"
        db_table = 'rbac_menu'
        unique_together = [('name','url'),]

    def get_next_child_key(self):
        mark = self.child_mark
        self.child_mark += 1
        self.save()
        return "{}:{}".format(self.key, mark)

    @property
    def assist_url_list(self):
        try:
            return self.assist_url.split('\r\n')
        except:
            return []

class Permission2Group(models.Model):
    target = models.ForeignKey(UserGroup, on_delete=models.CASCADE, verbose_name='用户组')
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, verbose_name='菜单')
    action = models.CharField(max_length=50, verbose_name='操作')

    class Meta:
        verbose_name = "用户组权限"
        db_table = 'rbac_permission_group'
        unique_together = [('target','menu'),]

    @property
    def action_list(self):
        try:
            return eval(self.action)
        except:
            return self.action.split('')

class Permission2User(models.Model):
    target = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, verbose_name='菜单')
    action = models.CharField(max_length=50, verbose_name='操作')

    class Meta:
        verbose_name = "用户权限"
        db_table = 'rbac_permission_user'
        unique_together = [('target','menu'),]



    @property
    def action_list(self):
        try:
            return eval(self.action)
        except:
            return self.action.split(' ')