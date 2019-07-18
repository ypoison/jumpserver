# -*- coding: utf-8 -*-
#

from celery import shared_task

from common.utils import get_logger
from django.db import transaction

from audits.models import OperateLog

logger = get_logger(__name__)

@shared_task
def write_log_async(**data):
    with transaction.atomic():
        try:
            OperateLog.objects.create(**data)
        except Exception as e:
            logger.error("Config node operate log error: {}".format(e))