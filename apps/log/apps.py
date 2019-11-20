from __future__ import unicode_literals

from django.apps import AppConfig


class LogConfig(AppConfig):
    name = 'log'

    def ready(self):
        #from . import signals_handler
        super().ready()
