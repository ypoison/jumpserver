from __future__ import unicode_literals

from django.apps import AppConfig


class ConfigConfig(AppConfig):
    name = 'config'

    def ready(self):
        #from . import signals_handler
        super().ready()
