from __future__ import unicode_literals

from django.apps import AppConfig


class LogMisConfig(AppConfig):
    name = 'log_mis'

    def ready(self):
        #from . import signals_handler
        super().ready()
