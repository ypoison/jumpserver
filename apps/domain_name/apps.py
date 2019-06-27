from __future__ import unicode_literals

from django.apps import AppConfig


class DomainNameConfig(AppConfig):
    name = 'domain_name'

    def ready(self):
        #from . import signals_handler
        super().ready()
