#!/usr/bin/env python
#coding=utf-8

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException

'''获取域名列表'''
from aliyunsdkdomain.request.v20180129.QueryDomainListRequest import QueryDomainListRequest
from aliyunsdkalidns.request.v20150109.DescribeDomainsRequest import DescribeDomainsRequest
'''获取解析记录列表'''
from aliyunsdkalidns.request.v20150109.DescribeDomainRecordsRequest import DescribeDomainRecordsRequest
'''添加记录'''
from aliyunsdkalidns.request.v20150109.AddDomainRecordRequest import AddDomainRecordRequest
'''修改记录'''
from aliyunsdkalidns.request.v20150109.UpdateDomainRecordRequest import UpdateDomainRecordRequest
'''删除记录'''
from aliyunsdkalidns.request.v20150109.DeleteDomainRecordRequest import DeleteDomainRecordRequest
'''修改记录状态'''
from aliyunsdkalidns.request.v20150109.SetDomainRecordStatusRequest import SetDomainRecordStatusRequest
'''添加域名'''
from aliyunsdkalidns.request.v20150109.AddDomainRequest import AddDomainRequest


import json

class AliyunDomainName:
    """docstring for AliyunDomainName"""

    def get_domain_name_list(self, obj):
        self.client = AcsClient(
        obj.access_id,
        obj.access_key,
        'cn-hangzhou')
        request = QueryDomainListRequest()
        request.set_accept_format('json')
        
        request.set_PageSize(100)
        request.set_PageNum(1)
        try:
            response = self.client.do_action_with_exception(request)
            ret = json.loads(str(response, encoding='utf-8'))['Data']['Domain']

            request = DescribeDomainsRequest()
            request.set_accept_format('json')
            
            request.set_PageSize(100)

            response = self.client.do_action_with_exception(request)
            DescribeDomains = json.loads(str(response, encoding='utf-8'))['Domains']['Domain']
            domains = []
            for r in ret:
                domains.append(r['DomainName'])
            for d in DescribeDomains:
                if d['DomainName'] not in domains:
                    ret.append(d)

            return {'code':1,'message':ret}
        except Exception as e:
            return {'code':0,'message':e}

    def add_domain_name(self,obj):
        self.client = AcsClient(
        obj.account.access_id,
        obj.account.access_key,
        'cn-hangzhou')
        request = AddDomainRequest()
        request.set_accept_format('json')

        request.set_DomainName(obj.domain_name)
        try:
            response = self.client.do_action_with_exception(request)
            ret = json.loads(str(response, encoding='utf-8'))
            return {'code':1,'message':ret}
        except Exception as e:
            return {'code':0,'message':e}

    def get_domain_name_records(self,obj):
        self.client = AcsClient(
        obj.account.access_id,
        obj.account.access_key,
        'cn-hangzhou')
        request = DescribeDomainRecordsRequest()
        request.set_accept_format('json')
        
        request.set_PageSize(100)
        request.set_DomainName(obj.domain_name)
        
        try:
            response = self.client.do_action_with_exception(request)
            ret = json.loads(str(response, encoding='utf-8'))['DomainRecords']['Record']
            return {'code':1,'message':ret}
        except Exception as e:
            return {'code':0,'message':e}

    def add_record(self,obj):
        self.client = AcsClient(
        obj.domain_name.account.access_id,
        obj.domain_name.account.access_key,
        'cn-hangzhou')
        request = AddDomainRecordRequest()
        request.set_accept_format('json')

        request.set_TTL(obj.ttl)
        request.set_Line(obj.line)
        request.set_Value(obj.value)
        request.set_Type(obj.type)
        request.set_RR(obj.rr)
        request.set_DomainName(obj.domain_name.domain_name)
        if obj.priority:
            request.set_Priority(obj.priority)

        try:
            response = self.client.do_action_with_exception(request)
            ret = json.loads(str(response, encoding='utf-8'))
            return {'code':1,'message':ret}
        except Exception as e:
            return {'code':0,'message':e}

    def update_record(self,obj):
        self.client = AcsClient(
        obj.domain_name.account.access_id,
        obj.domain_name.account.access_key,
        'cn-hangzhou')
        request = UpdateDomainRecordRequest()
        request.set_accept_format('json')
        
        request.set_RecordId(obj.record_id)
        request.set_TTL(obj.ttl)
        request.set_Line(obj.line)
        request.set_Value(obj.value)
        request.set_Type(obj.type)
        request.set_RR(obj.rr)
        if obj.priority:
            request.set_Priority(obj.priority)
        
        try:
            response = self.client.do_action_with_exception(request)
            ret =  json.loads(str(response, encoding='utf-8'))
            return {'code':1,'message':ret}
        except Exception as e:
            return {'code':0,'message':e}

    def del_record(self,obj):
        self.client = AcsClient(
        obj.domain_name.account.access_id,
        obj.domain_name.account.access_key,
        'cn-hangzhou')
        request = DeleteDomainRecordRequest()
        request.set_accept_format('json')
        
        request.set_RecordId(obj.record_id)
        
        try:
            response = self.client.do_action_with_exception(request)
            ret =  json.loads(str(response, encoding='utf-8'))
            return {'code':1,'message':ret}
        except Exception as e:
            return {'code':0,'message':e}

    def set_record_status(self,obj):
        self.client = AcsClient(
        obj.domain_name.account.access_id,
        obj.domain_name.account.access_key,
        'cn-hangzhou')
        request = SetDomainRecordStatusRequest()
        request.set_accept_format('json')
        
        request.set_Status(obj.status)
        request.set_RecordId(obj.record_id)
        
        try:
            response = self.client.do_action_with_exception(request)
            ret =  json.loads(str(response, encoding='utf-8'))
            return {'code':1,'message':ret}
        except Exception as e:
            return {'code':0,'message':e}




if __name__ == '__main__':
    a=AliyunDomainName()
    #print(a.ali_get_domain_name_list)
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