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
__all__ = ['CDNDomainViewSet','CDNDomainUpdateApi','CDNDomainSetApi',
           'CDNFreshSetApi',
           ]
SetCDN = AliyunCDN()

class CDNDomainViewSet(BulkModelViewSet):
    filter_fields = ("domain_name",)
    search_fields = filter_fields
    queryset = CDNDomain.objects.all()
    permission_classes = (IsOrgAdmin,)
    serializer_class = serializers.CDNDomainSerializer
    pagination_class = LimitOffsetPagination

class CDNDomainUpdateApi(APIView):
    permission_classes = (IsOrgAdmin,)

    def get(self, request, *args, **kwargs):
        cdn_id = self.kwargs.get('pk')
        cdn = get_object_or_none(CDNDomain,id=cdn_id)
        data = {
            'access_id': cdn.account.access_id,
            'access_key': cdn.account.access_key,
            'domain_name':cdn.domain_name
        }
        cdn_data = SetCDN.get_cdn_list(**data)
        if cdn_data['code']:
            req = cdn_data['msg'][0]
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
                source_list.append('%s:%s' % (s['Content'],s['Priority']))
            cdn.sources =str(source_list)
            cdn.save()
        else:
            return Response({'error': '%s:%s' % (cdn.domain_name,cdn_data['msg'])}, status=400)
        return Response({"msg": "ok"})

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

class CDNFreshSetApi(APIView):
    permission_classes = (IsOrgAdmin,)

    def get(self, request, *args, **kwargs):
        accounts = Account.objects.all()
        for account in accounts:
            try:
                auth_list = eval(account.auth)
            except:
                auth_list = account.auth.split(' ')
            if 'cdn' in auth_list:
                data = {
                    'access_id': account.access_id,
                    'access_key': account.access_key,
                }
                fresh_data = SetCDN.fresh_get(**data)
                if fresh_data['code']:
                    return Response({"results": fresh_data['msg']})