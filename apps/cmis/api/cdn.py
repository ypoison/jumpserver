# ~*~ coding: utf-8 ~*~

from rest_framework_bulk import BulkModelViewSet
from rest_framework.views import APIView, Response
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import generics

from common.utils import get_logger, get_object_or_none
from common.permissions import IsOrgAdmin

from ..models import CDNDomain, Account
from .. import serializers

from ..aliyun import AliyunCDN

import time

logger = get_logger(__file__)
__all__ = ['CDNDomainViewSet','CDNDomainModifyApi', 'CDNDomainUpdateApi','CDNDomainSetApi',
           'CDNFreshSetApi',
           'OSSGetApi',
           ]
SetCDN = AliyunCDN()

class CDNDomainViewSet(BulkModelViewSet):
    filter_fields = ("domain_name",)
    search_fields = filter_fields
    queryset = CDNDomain.objects.all()
    permission_classes = (IsOrgAdmin,)
    serializer_class = serializers.CDNDomainSerializer
    pagination_class = LimitOffsetPagination

class CDNDomainModifyApi(APIView):
    permission_classes = (IsOrgAdmin,)

    def post(self, request, *args, **kwargs):
        cdn_id = self.kwargs.get('pk')
        req = self.request.data
        cdn = get_object_or_none(CDNDomain, id=cdn_id)
        data = {
            'access_id': cdn.account.access_id,
            'access_key': cdn.account.access_key,
            'domain_name': cdn.domain_name,
            'source_type': req.get('source_type'),
            'source_port': req.get('source_port'),
            'sources': req.get('sources'),
        }
        print(data)
        cdn_data = SetCDN.cdn_modify(**data)
        print(cdn_data)
        if cdn_data['code']:
            cdn.source_type = req.get('source_type')
            cdn.source_port = req.get('source_port')
            cdn.sources = req.get('sources')
            cdn.save()
            return Response({"msg": "ok"})
        else:
            return Response({'error': '%s' % (cdn_data['msg'])}, status=400)

class CDNDomainUpdateApi(APIView):
    permission_classes = (IsOrgAdmin,)

    def cdn_update(self, cdn, **data):
        cdn_data = SetCDN.get_cdn_list(**data)
        if cdn_data['code']:
            for req in cdn_data['msg']:
                cdn.cname = req['Cname']
                cdn.cdn_type = req['CdnType']
                cdn.domain_status = req['DomainStatus']
                cdn.https = req['SslProtocol']
                cdn.domain_name = req['DomainName']
                source = req['Sources']['Source']
                cdn.source_type = source[0]['Type']
                cdn.source_port = source[0]['Port']
                cdn.gmt_created = req['GmtCreated']
                source_list = []
                for s in source:
                    source_list.append('%s:%s' % (s['Content'], s['Priority']))
                cdn.sources = ','.join(source_list)
                cdn.save()
        return cdn_data

    def post(self, request, *args, **kwargs):
        cdn_id = self.kwargs.get('pk')
        action = self.request.data.get('action')
        if action == 'full':
            accounts = Account.objects.all()
            for account in accounts:
                if 'cdn' in account.auth_list:
                    data = {
                        'access_id': account.access_id,
                        'access_key': account.access_key,
                    }
                    cdn_list = [ c.domain_name for c in CDNDomain.objects.filter(account=account)]
                    cdn_data = SetCDN.get_cdn_list(**data)
                    if cdn_data['code']:
                        domain_name_list = []
                        for req in cdn_data['msg']:
                            domain_name = req['DomainName']
                            domain_name_list.append(domain_name)
                            if domain_name in cdn_list:
                                cdn = CDNDomain.objects.get(account=account,domain_name=domain_name)
                                cdn.cname = req['Cname']
                                cdn.cdn_type = req['CdnType']
                                cdn.domain_status = req['DomainStatus']
                                cdn.https = req['SslProtocol']
                                cdn.domain_name = domain_name
                                source = req['Sources']['Source']
                                cdn.source_type = source[0]['Type']
                                cdn.source_port = source[0]['Port']
                                cdn.gmt_created = req['GmtCreated']
                                source_list = []
                                for s in source:
                                    source_list.append('%s:%s' % (s['Content'], s['Priority']))
                                cdn.sources = ','.join(source_list)
                                cdn.save()
                            else:
                                source = req['Sources']['Source']
                                source_list = []
                                for s in source:
                                    source_list.append('%s:%s' % (s['Content'], s['Priority']))
                                    CDNDomain.objects.create(
                                        account=account,
                                        cname = req['Cname'],
                                        cdn_type = req['CdnType'],
                                        domain_status = req['DomainStatus'],
                                        https = req['SslProtocol'],
                                        domain_name = domain_name,
                                        source_type = source[0]['Type'],
                                        source_port = source[0]['Port'],
                                        gmt_created = req['GmtCreated'],
                                        sources = str(source_list)
                                    )
                        for r in CDNDomain.objects.filter(account=account):
                            if r.domain_name not in domain_name_list:
                                r.delete()
                        return Response({"msg": "ok"})
                    else:
                        Response({'error': '%s:%s' % (cdn.domain_name, cdn_data['msg'])}, status=400)

        cdn = get_object_or_none(CDNDomain, id=cdn_id)
        data = {
            'access_id': cdn.account.access_id,
            'access_key': cdn.account.access_key,
            'domain_name': cdn.domain_name
        }
        if action == 'update':
            cdn_data = self.cdn_update(cdn, **data)
        elif action == 'start':
            cdn_data = SetCDN.start(**data)
            time.sleep(2)
            self.cdn_update(cdn, **data)
        elif action == 'delete':
            cdn_data = SetCDN.delete(**data)
            if cdn_data['code']:
                cdn.delete()
        elif action == 'stop':
            cdn_data = SetCDN.stop(**data)
            time.sleep(2)
            self.cdn_update(cdn, **data)

        else:
            Response({'error': '缺乏参数'}, status=400)
        if cdn_data['code']:
            return Response({"msg": "ok"})
        else:
            Response({'error': '%s:%s' % (cdn.domain_name, cdn_data['msg'])}, status=400)

class CDNDomainSetApi(APIView):
    permission_classes = (IsOrgAdmin,)

    def post(self, request, *args, **kwargs):
        cdn_id = self.kwargs.get('pk')
        action = self.request.data.get('action')
        https = self.request.data.get('https')
        if https:
            https = 'on'
        else:
            https = 'off'

        cdn = get_object_or_none(CDNDomain, id=cdn_id)
        data = {
            'access_id': cdn.account.access_id,
            'access_key': cdn.account.access_key,
            'domain_name': cdn.domain_name
        }
        if action == 'https':
            data['https'] = https
            data['CertType'] = self.request.data.get('CertType')
            data['CertName'] = self.request.data.get('CertName')
            data['ServerCertificate'] = self.request.data.get('ServerCertificate')
            data['PrivateKey'] = self.request.data.get('PrivateKey')
            cdn_data = SetCDN.set_https(**data)
            if cdn_data['code']:
                time.sleep(3)
                cdn_data = SetCDN.cert_check(**data)
                if cdn_data['code']:
                    cdn.https = cdn_data['msg']['ServerCertificateStatus']
                    cdn.save()
                    return Response({"msg": cdn_data['msg']})
                else:
                    return Response({'error': '%s' % (cdn_data['msg'])}, status=400)
            else:
                return Response({'error': '%s' % (cdn_data['msg'])}, status=400)

        elif action == 'checkCert':
            cdn_data = SetCDN.cert_check(**data)
            if cdn_data['code']:
                cdn.https = cdn_data['msg']['ServerCertificateStatus']
                cdn.save()
                return Response({"msg": cdn_data['msg']})
            else:
                return Response({'error': '%s' % (cdn_data['msg'])}, status=400)
        else:
            Response({'error': '缺乏参数'}, status=400)
        return Response({"msg": "ok"})

class OSSGetApi(APIView):
    permission_classes = (IsOrgAdmin,)

    def get(self, request, *args, **kwargs):
        cdn_id = self.kwargs.get('pk')
        account = Account.objects.get(id=cdn_id)
        data = {
            'access_id': account.access_id,
            'access_key': account.access_key,
        }
        oss_data = SetCDN.oss_get(**data)
        return Response(oss_data)

class CDNFreshSetApi(APIView):
    permission_classes = (IsOrgAdmin,)

    def get(self, request, *args, **kwargs):
        accounts = Account.objects.all()
        for account in accounts:
            if 'cdn' in account.auth_list:
                data = {
                    'access_id': account.access_id,
                    'access_key': account.access_key,
                }
                fresh_data = SetCDN.fresh_get(**data)
                if fresh_data['code']:
                    return Response({"results": fresh_data['msg']})