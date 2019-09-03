# -*- coding: utf-8 -*-
#

from celery import shared_task

from common.utils import get_logger, get_object_or_none
from django.db import transaction
from audits.models import OperateLog
from .models import App, WEBConfigRecords
from .webconfig import WEBConfig

webconfig = WEBConfig()
logger = get_logger(__name__)

@shared_task
def write_log_async(**data):
    with transaction.atomic():
        try:
            OperateLog.objects.create(**data)
        except Exception as e:
            logger.error("Config node operate log error: {}".format(e))

@shared_task
def bulk_config(req):
    game_domain = req.get('game_domain', '')
    pay_domain = req.get('pay_domain', '')
    h5_domain = req.get('h5_domain', '')
    net_type = req['net_type']
    node_asset = req['node_asset']
    node_ip = node_asset.ip
    platform = req['platform']
    pf_code = platform.code

    proxy_assets_list = platform.get_all_assets()
    jid = bulk_config.request.id
    for proxy_asset in proxy_assets_list:
        try:
            asset_name = proxy_asset.hostname.split('-')[-1]
            if 'Games' in asset_name and game_domain:
                domain = game_domain
                comment = proxy_asset.hostname
            elif asset_name == 'HallServer' and h5_domain:
                domain = h5_domain
                comment = '{}-H5'.format(pf_code)
            elif asset_name == 'ApiServer' and pay_domain:
                domain = pay_domain
                comment = '{}-Pay'.format(pf_code)
            else:
                continue
            if net_type == 'intranet':
                proxyip = proxy_asset.ip
            else:
                proxyip = proxy_asset.public_ip

            config_record = WEBConfigRecords.objects.create(
                domain=domain,
                jid=jid
            )
            port = proxyport = get_object_or_none(App, name=asset_name).port

            config_record.platform = platform
            config_record.node_asset = node_asset
            config_record.port = port
            config_record.proxy_asset = proxy_asset
            config_record.proxy_ip = proxyip
            config_record.proxy_port = proxyport
            config_record.comment = comment
            config_record.save()
        except Exception as e:
            config_record.comment = e
            config_record.save()

        kwargs = {
            'platform': pf_code,
            'node_ip': node_ip,
            'port': port,
            'domain': domain,
            'proxy_ip': proxyip,
            'proxy_port': proxyport,
            'comment': comment
        }
        add_web_config = webconfig.add(**kwargs)
        if not add_web_config['code']:
            config_record.comment = 'error:{}'.format(add_web_config['msg'])
            config_record.save()