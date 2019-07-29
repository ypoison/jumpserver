#!/usr/bin/env python
#coding=utf-8

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException

from aliyunsdkcdn.request.v20180510.DescribeUserDomainsRequest import DescribeUserDomainsRequest
from aliyunsdkcdn.request.v20180510.AddCdnDomainRequest import AddCdnDomainRequest


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


if __name__ == '__main__':
    a=AliyunCDN()
    data = {
        'access_id':'LTAIsqupmY8GlhNG',
        'access_key':'YHsR8d6P6ouRP7Vk2kKVDFBUzROlXw'
    }
    print(a.get_cdn_list(**data))
    #[{“content”:”1.1.1.1”, ”type”:”ipaddr”, ”priority”:”20”, ”port”:80,”weight”:”15”}]
    #{'domain_name': 'vvvi.com',  'scope': 'domestic', 'source_port': 80, 'source_type': 'ipaddr', 'sources': '1.1.1.1:20,2.1.1.1:30', 'domain_status': None, 'comment': ''}

    #print(a.ali_get_domain_name_dns('yvnwq.cn'))
    #b=a.update_record(
    #    RecordId='17838107624944640',
    #    ttl=600,
    #    line='default',
    #    value='192.168.11.169',
    #    type='A',
    #    rr='dytest',
    #    priority=''
    #    )
    #print(b)