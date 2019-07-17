# ~*~ coding: utf-8 ~*~
from celery import shared_task
from common.utils import (get_logger)
from ops.celery.decorator import (
    register_as_period_task, after_app_shutdown_clean_periodic
)

from .models import DomainName
from .check_gfw import CheckGFW
from .beian import beian

import time

logger = get_logger(__file__)
CheckGFW = CheckGFW()
BeiAnCheck=beian()


@shared_task
@register_as_period_task(interval=86400)
def check_GFW():
    ch_lose_list = []
    try:
        DomainNames = DomainName.objects.all()
        for domain in DomainNames:
            check = CheckGFW.check_gfw(domain.domain_name)
            status = check['code']
            if status == -1:
                logger.error(check['msg'])
                time.sleep(1)
            else:
                if not status:
                    ch_lose_list.append(domain.domain_name)
                domain.ch_lose = status
                domain.save()
                time.sleep(1)
    except Exception as e:
        logger.error(check['msg'])
    return '被墙域名:%s' % ch_lose_list

@shared_task
@register_as_period_task(interval=86400)
def check_beian():
    lose_list = []
    try:
        DomainNames = DomainName.objects.all()
        for domain in DomainNames:
            beian_check = BeiAnCheck.check_beian(domain.domain_name)
            code = beian_check.get('code')
            if code == -1:
                logger.error(check['msg'])
                time.sleep(1)
            else:
                if not code:
                    lose_list.append(domain.domain_name)
                if domain.beian != 2:
                    domain.beian = code
                    domain.save()
                    logger.info('task:check_beian:%s' % beian_check)
                    time.sleep(1)

    except Exception as e:
        logger.error(check['msg'])
    return '掉备案域名:%s' % lose_list