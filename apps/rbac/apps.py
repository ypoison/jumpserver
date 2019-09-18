from __future__ import unicode_literals

from django.apps import AppConfig


class RBACConfig(AppConfig):
    name = 'rbac'

    def ready(self):
        super().ready()