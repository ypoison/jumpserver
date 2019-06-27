# ~*~ coding: utf-8 ~*~
import json
import re
import os

from celery import shared_task
from django.utils.translation import ugettext as _
from django.core.cache import cache

from common.utils import (
    capacity_convert, sum_capacity, encrypt_password, get_logger
)
from ops.celery.decorator import (
    register_as_period_task, after_app_shutdown_clean_periodic
)

from .models import SystemUser, AdminUser, Asset
from . import const


FORKS = 10
TIMEOUT = 60
logger = get_logger(__file__)
CACHE_MAX_TIME = 60*60*2
disk_pattern = re.compile(r'^hd|sd|xvd|vd')
PERIOD_TASK = os.environ.get("PERIOD_TASK", "on")



@shared_task
@register_as_period_task(interval=30)
def check_GWF():
    """
    A period task that update the ansible task period
    """
    print(11111111111111111111111)
    return True