from __future__ import unicode_literals

from django.apps import AppConfig


class BackupConfig(AppConfig):
    name = 'backup'

    def ready(self):
        #from . import signals_handler
        super().ready()
