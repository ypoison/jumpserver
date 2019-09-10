from __future__ import unicode_literals

from django.apps import AppConfig


class CMisConfig(AppConfig):
    name = 'cmis'

    def ready(self):
        super().ready()