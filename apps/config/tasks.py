# -*- coding: utf-8 -*-
#

from celery import shared_task

from common.utils import get_logger, get_object_or_none
from django.db import transaction
from audits.models import OperateLog

from assets.models import Asset, Node

from .models import App, WEBConfigRecords
from .webconfig import WEBConfig

webconfig = WEBConfig()
logger = get_logger(__name__)

def save_config(**req):
    net_type = req.pop('net_type')
    jid = req.pop('jid')
    node_asset = req.pop('node_asset')
    app = req.pop('app')
    proxy_asset = req.pop('proxy_asset')
    platform = req['platform']
    domain = req['domain']
    comment = req['comment']

    if net_type == 'intranet':
        proxyip = req['proxy_ip'] = proxy_asset.ip
    else:
        proxyip = req['proxy_ip'] = proxy_asset.public_ip

    port = proxyport = req['port'] = req['proxy_port'] = app.port

    try:
        config_record = get_object_or_none(WEBConfigRecords, node_asset=node_asset, domain=domain, port=port)
    except:
        config_record = WEBConfigRecords.objects.create(
            platform=platform,
            node_asset=node_asset,
            port=port,
            domain=domain,
            jid=jid,
            comment='{}:{}'.format(proxy_asset, '此记录有重复，请先删除错误的记录')
        )
        return
    if config_record:
        config_record.jid = jid
    else:
        config_record = WEBConfigRecords.objects.create(
            platform=platform,
            node_asset=node_asset,
            port=port,
            domain=domain,
            jid=jid
        )

    config_record.platform = platform
    config_record.node_asset = node_asset
    config_record.port = port
    config_record.proxy_asset = proxy_asset
    config_record.proxy_ip = proxyip
    config_record.proxy_port = proxyport
    config_record.comment = comment
    config_record.save()

    req['platform'] = req.pop('pf_code')
    req['node_ip'] = node_asset.ip
    add_web_config = webconfig.add(**req)
    if not add_web_config['code']:
        config_record.comment = 'error:{}'.format(add_web_config['msg'])
        config_record.save()

@shared_task
def write_log_async(**data):
    with transaction.atomic():
        try:
            OperateLog.objects.create(**data)
        except Exception as e:
            logger.error("Config node operate log error: {}".format(e))

@shared_task
def bulk_config(req):
    jid = bulk_config.request.id
    req['jid'] = jid
    game_domain = req.pop('game_domain', '')
    pay_domain = req.pop('pay_domain', '')
    h5_domain = req.pop('h5_domain', '')
    platform = req['platform']
    pf_code = req['pf_code'] = platform.code
    if game_domain:
        req['domain'] = game_domain
        games = req.pop('games')
        if games:
            games = App.objects.filter(name__in=games)
        else:
            games = App.objects.filter(type='game')
        node_id = Node.objects.get(key__regex='^{0}:[0-9]+$'.format(platform.key), value='games').id
        for game in games:
            req['app'] = game
            proxy_asset = get_object_or_none(Asset, nodes__id=node_id, hostname='{}-{}'.format(pf_code, game.name))
            if not proxy_asset:
                proxy_asset = get_object_or_none(Asset, nodes__id=node_id, hostname='{}-{}'.format(pf_code, 'GameServer'))
            if proxy_asset:
                req['proxy_asset'] = proxy_asset
                req['comment'] = '{}-{}'.format(pf_code, game.name)
                save_config(**req)
    if pay_domain:
        asset_name = 'ApiServer'
        app_name = 'Pay'
        req['domain'] = pay_domain
        node_id = Node.objects.get(key__regex='^{0}:[0-9]+$'.format(platform.key), value='other').id
        req['app'] = get_object_or_none(App, type='other', name=app_name)
        proxy_asset = get_object_or_none(Asset, nodes__id=node_id, hostname='{}-{}'.format(pf_code, asset_name))
        if proxy_asset:
            req['proxy_asset'] = proxy_asset
            req['comment'] = '{}-{}'.format(pf_code, app_name)
            save_config(**req)
    if h5_domain:
        asset_name = 'HallServer'
        app_name = 'H5'
        req['domain'] = h5_domain
        node_id = Node.objects.get(key__regex='^{0}:[0-9]+$'.format(platform.key), value='other').id
        req['app'] = get_object_or_none(App, type='other', name=app_name)
        proxy_asset = get_object_or_none(Asset, nodes__id=node_id, hostname='{}-{}'.format(pf_code, asset_name))
        if proxy_asset:
            req['proxy_asset'] = proxy_asset
            req['comment'] = '{}-{}'.format(pf_code, app_name)
            save_config(**req)