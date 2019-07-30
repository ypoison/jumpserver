#!/usr/bin/env python
#coding=utf-8

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException

from aliyunsdkcdn.request.v20180510.DescribeUserDomainsRequest import DescribeUserDomainsRequest
from aliyunsdkcdn.request.v20180510.AddCdnDomainRequest import AddCdnDomainRequest
from aliyunsdkcdn.request.v20180510.SetDomainServerCertificateRequest import SetDomainServerCertificateRequest
from aliyunsdkcdn.request.v20180510.DescribeDomainCertificateInfoRequest import DescribeDomainCertificateInfoRequest
from aliyunsdkcdn.request.v20180510.RefreshObjectCachesRequest import RefreshObjectCachesRequest
from aliyunsdkcdn.request.v20180510.PushObjectCacheRequest import PushObjectCacheRequest
from aliyunsdkcdn.request.v20180510.DescribeRefreshTasksRequest import DescribeRefreshTasksRequest


import json

class AliyunCDN:
    """docstring for AliyunDomainName"""

    def get_cdn_list(self, **kwargs):
        self.client = AcsClient(
        kwargs['access_id'],
        kwargs['access_key'],
        'cn-hangzhou')
        request = DescribeUserDomainsRequest()
        request.set_accept_format('json')
        request.set_PageSize(100)

        domain_name = kwargs.get('domain_name', '')
        if domain_name:
            request.set_DomainName(domain_name)
        try:
            response = self.client.do_action_with_exception(request)
            ret = json.loads(str(response, encoding='utf-8'))
            return {'code':1,'msg':ret['Domains']['PageData']}
        except Exception as e:
            return {'code':0,'msg':e}

    def cdn_create(self, **kwargs):
        self.client = AcsClient(
            kwargs['access_id'],
            kwargs['access_key'],
            'cn-hangzhou')

        request = AddCdnDomainRequest()
        request.set_accept_format('json')
        sources = kwargs['sources'].split(',')
        source_list = []
        for source in sources:
            source = source.split(':')
            content = source[0]
            priority = source[1]
            source_dict = {
                'content': content,
                'type': kwargs['source_type'],
                'priority':priority,
            }
            source_list.append(source_dict)
        request.set_CdnType(kwargs['cdn_type'])
        request.set_DomainName(kwargs['domain_name'])
        request.set_Sources(source_list)
        request.set_Scope(kwargs['scope'])
        if kwargs['check_url']:
            request.set_CheckUrl(kwargs['check_url'])

        try:
            response = self.client.do_action_with_exception(request)
            ret = json.loads(str(response, encoding='utf-8'))
            return {'code':1,'msg':ret}
        except Exception as e:
            return {'code':0,'msg':e}

    def set_https(self, **kwargs):
        self.client = AcsClient(
        kwargs['access_id'],
        kwargs['access_key'],
        'cn-hangzhou')

        request = SetDomainServerCertificateRequest()
        request.set_accept_format('json')

        request.set_DomainName(kwargs['domain_name'])
        request.set_ServerCertificateStatus(kwargs['https'])
        request.set_CertType("free")

        try:
            response = self.client.do_action_with_exception(request)
            ret = json.loads(str(response, encoding='utf-8'))
            return {'code':1,'msg':ret['RequestId']}
        except Exception as e:
            return {'code':0,'msg':e}

    def cert_check(self,**kwargs):
        self.client = AcsClient(
        kwargs['access_id'],
        kwargs['access_key'],
        'cn-hangzhou')

        request = DescribeDomainCertificateInfoRequest()
        request.set_accept_format('json')

        request.set_DomainName(kwargs['domain_name'])

        try:
            response = self.client.do_action_with_exception(request)
            ret = json.loads(str(response, encoding='utf-8'))
            ret = ret["CertInfos"]["CertInfo"][0]
            status = {'success': '已生效。',
                    'checking': '检测域名是否在阿里云CDN。',
                    'cname_error': '域名没有切到阿里云CDN。',
                    'top_domain_cname_error': '顶级域名没有切到阿里云CDN。',
                    'domain_invalid': '域名包含非法字符。',
                    'unsupport_wildcard': '不支持泛域名。',
                    'applying': '证书申请中。',
                    'get_token_timeout': '证书申请超时。',
                    'check_token_timeout': '校验超时。',
                    'get_cert_timeout': '获取证书超时。',
                    'failed': '证书申请失败。',
            }
            if ret['Status']:
                ret_status = status[str(ret['Status'])]
            else:
                ret_status = ''
            msg = {'ServerCertificateStatus':ret['ServerCertificateStatus'],'Status':ret_status}
            return {'code':1,'msg':msg}
        except Exception as e:
            return {'code':0,'msg':e}

    def fresh_set(self, **kwargs):
        self.client = AcsClient(
        kwargs['access_id'],
        kwargs['access_key'],
        'cn-hangzhou')

        if kwargs['action'] == 'PushCache':
            request = PushObjectCacheRequest()
        elif kwargs['action'] == 'RefreshCaches':
            request = RefreshObjectCachesRequest()
        else:
            return {'code': 0, 'msg': 'action?'}
        print(kwargs)
        request.set_accept_format('json')
        request.set_ObjectPath(kwargs['ObjectPath'])
        request.set_ObjectType(kwargs['ObjectType'])
        #try:
        response = self.client.do_action_with_exception(request)
        ret = json.loads(str(response, encoding='utf-8'))
        return {'code':1}
        #except Exception as e:
        #    return {'code':0,'msg':e}

    def fresh_get(self, **kwargs):
        self.client = AcsClient(
        kwargs['access_id'],
        kwargs['access_key'],
        'cn-hangzhou')

        request = DescribeRefreshTasksRequest()
        request.set_accept_format('json')

        try:
            response = self.client.do_action_with_exception(request)
            ret = json.loads(str(response, encoding='utf-8'))
            return {'code':1,'msg':ret['Tasks']['CDNTask']}
        except Exception as e:
            return {'code':0,'msg':e}

if __name__ == '__main__':
    a=AliyunCDN()
    data = {
        'access_id':'LTAIsqupmY8GlhNG',
        'access_key':'YHsR8d6P6ouRP7Vk2kKVDFBUzROlXw',
        'domain_name': 'image1.vivi.com',
        'https': 'on'
    }
    print(a. set_https(**data))