# ~*~ coding: utf-8 ~*~
import time

from celery import shared_task
from common.utils import get_logger, get_object_or_none

from assets.models import Asset
from cmis.models import ChostCreateRecord
from . import ucloud_api

logger = get_logger(__file__)
cloud_api = ucloud_api.UcloudAPI()

def set_info(queryset):
    if queryset['code']:
        data = queryset['msg']
        for ip in data['IPSet']:
            if ip['Type'] == 'BGP' or ip['Type'] == 'International':
                asset = get_object_or_none(Asset, number=data['UHostId'])
                if asset:
                    asset.public_ip = ip['IP']
                    asset.is_active = True
                    asset.save()
        create_record = get_object_or_none(ChostCreateRecord, hid=data['UHostId'])
        create_record.status=data['State']
        create_record.save()
    else:
        logger.error(queryset['msg'])

@shared_task
def buyer(create_record, **kw):
    admin_user = kw.pop('admin_user')
    nodes = kw.pop('nodes')
    port = kw.pop('SSHPort')
    domain = kw.pop('Domain')
    queryset = cloud_api.CreateUhostInstance(**kw)
    if queryset['code']:
        data = queryset['msg']
        ip = data['IPs'][0]
        cid = data['UHostIds'][0]
        try:
            asset = Asset.objects.create(
                hostname=kw.get('Name'),
                platform=kw.get('OSType'),
                ip=ip,
                port=port,
                domain=domain,
                admin_user=admin_user,
                number=cid,
                comment='由云账号"%s"采购添加' % create_record.account,
                is_active=False,
            )
            asset.nodes.set(nodes)

            create_record.hid = cid
            create_record.asset = asset
            create_record.save()
            time.sleep(10)
            kwargs = {
                'PrivateKey': create_record.account.access_key,
                'PublicKey': create_record.account.access_id,
                'Region': kw['Region'],
                'ProjectId': kw['ProjectId'],
                'UHostIds.0': cid
            }
            queryset = cloud_api.GetUHostInstance(**kwargs)
            set_info(queryset)
        except Exception as e:
            create_record.status = e
            create_record.save()
    else:
        create_record.status = queryset['error']
        create_record.save()
        logger.error(queryset['error'])

@shared_task
def bulk_buyer(node_code, create_host_list, req, **kw):
    jid = bulk_buyer.request.id
    account = kw.pop('account')
    admin_user = req.pop('admin_user')
    nodes = req.pop('nodes')
    port = kw.pop('SSHPort')
    domain = req.pop('Domain')
    platform = kw.pop('OSType')

    for create_host in create_host_list:
        Name = kw['Name'] = '{0}-{1}'.format(node_code, create_host)
        create_record = ChostCreateRecord.objects.create(
            job_id=jid,
            region=kw['Region'],
            account_id=str(account.id)
        )
        check_host = get_object_or_none(Asset,hostname=Name)
        if check_host:
            create_record.status = '主机名为:{}已存在。'.format(Name)
            create_record.save()
            continue
        queryset = cloud_api.CreateUhostInstance(**kw)
        if queryset['code']:
            data = queryset['msg']
            ip = data['IPs'][0]
            cid = data['UHostIds'][0]
            try:
                asset = Asset.objects.create(
                    hostname=kw.get('Name'),
                    platform=platform,
                    ip=ip,
                    port=port,
                    domain=domain,
                    admin_user=admin_user,
                    number=cid,
                    comment='由云账号"%s"采购添加' % create_record.account,
                    is_active=False,
                )
                asset.nodes.set(nodes)
                create_record.hid = cid
                create_record.asset = asset
                create_record.save()
                time.sleep(2)
                kwargs = {
                    'PrivateKey': create_record.account.access_key,
                    'PublicKey': create_record.account.access_id,
                    'Region': kw['Region'],
                    'ProjectId': kw['ProjectId'],
                    'UHostIds.0': cid
                }
                queryset = cloud_api.GetUHostInstance(**kwargs)
                set_info(queryset)
            except Exception as e:
                create_record.status = e
                create_record.save()
        else:
            create_record.status = '{}:{}'.format(Name, queryset['error'])
            create_record.save()
            logger.error(queryset['error'])