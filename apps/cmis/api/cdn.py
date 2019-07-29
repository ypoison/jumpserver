# ~*~ coding: utf-8 ~*~

from rest_framework_bulk import BulkModelViewSet
from rest_framework.views import APIView, Response
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import generics

from common.utils import get_logger, get_object_or_none
from common.permissions import IsOrgAdmin

from ..models import CDNDomain
from .. import serializers

from ..aliyun import AliyunCDN

logger = get_logger(__file__)
__all__ = ['CDNDomainViewSet','CDNDomainUpdateApi',
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
        if cdn:
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
            return Response({'error': '%s:%s' % (account,domain_name_data['message'])}, status=400)
        return Response({"msg": "ok"})