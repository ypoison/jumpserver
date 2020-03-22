from __future__ import unicode_literals

from django.apps import AppConfig


class OnlineConfig(AppConfig):
    name = 'online'

    def ready(self):
        #from . import signals_handler
        super().ready()
