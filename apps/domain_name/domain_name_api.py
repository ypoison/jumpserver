#!/usr/bin/env python
#coding=utf-8

from .aliyun import AliyunDomainName

from .dnspod import DomainList, RecordList, RecordCreate, RecordModify, RecordRemove, RecordStatus, DomainCreate

AliyunDomainName = AliyunDomainName()

class DomainNameApi:
    
    def domain_name_list(self, obj):
        resolver = obj.resolver
        if resolver == 'aliyun':
            return AliyunDomainName.get_domain_name_list(obj)
        elif resolver == 'dnspod':
            api = DomainList(obj)
            ret = api()
            code = ret.get("status", {}).get("code")
            if code == "1":
                domains = (api().get("domains"))
                domain_list = []
                for domain in domains:
                    domain_dict = {}
                    domain_dict.update(dict(
                        DomainName=domain['name'],
                        ExpirationDate='',
                        RegistrationDate='',
                        DomainStatus=3
                        ))
                    domain_list.append(domain_dict)
                return {'code':1,'message':domain_list}
            else:
                return {'code':0,'message':ret.get("status", {}).get("message")}

    def domain_name_create(self, obj):
        resolver = obj.account.resolver
        if resolver == 'aliyun':
            return AliyunDomainName.add_domain_name(obj)
        elif resolver == 'dnspod':
            api = DomainCreate(obj=obj)
            ret = api()
            code = ret.get("status", {}).get("code")
            if code == "1":
                domain = ret.get("domain", {})
                domain_id = domain.get("id")
                return {'code':1,'message':{'DomianId':domain_id}}
            else:
                return {'code':0,'message':ret.get("status", {}).get("message")}

    def domain_name_records(self, obj):
        resolver = obj.account.resolver
        if resolver == 'aliyun':
            return AliyunDomainName.get_domain_name_records(obj)
        elif resolver == 'dnspod':
            api = RecordList(obj=obj)
            ret = api()
            code = ret.get("status", {}).get("code")
            if code == "1":
                records=ret.get("records")
                record_list = []
                for record in records:
                    record_dict = {}
                    if record['line_id'] == '0':
                        line = 'default'
                    elif record['line_id'] == '10=0':
                        line = 'telecom'
                    elif record['line_id'] == '10=1':
                        line = 'unicom'
                    elif record['line_id'] == '10=2':
                        line = 'mobile'
                    if record['enabled'] == '1':
                        status = 'ENABLE'
                    else:
                        status = 'DISABLE'
    
                    record_dict.update(dict(
                        RecordId=record['id'],
                        Type=record['type'],
                        RR=record['name'],
                        Line=line,
                        Value=record['value'],
                        TTL=record['ttl'],
                        Status=status,
                        Locked=''
                        ))
                    record_list.append(record_dict)
                return {'code':1, 'message':record_list}
            else:
                return {'code':0,'message':ret.get("status", {}).get("message")}

    def record_create(self, obj):
        resolver = obj.domain_name.account.resolver
        if resolver == 'aliyun':
            return AliyunDomainName.add_record(obj)
        elif resolver == 'dnspod':
            api = RecordCreate(obj=obj)
            ret = api()
            code = ret.get("status", {}).get("code")
            if code == "1":
                record = ret.get("record", {})
                record_id = record.get("id")
                return {'code':1, "message":{'RecordId':record_id}}
            else:
                return {'code':0,'message':ret.get("status", {}).get("message")}

    def record_modify(self, obj):
        resolver = obj.domain_name.account.resolver
        if resolver == 'aliyun':
            return AliyunDomainName.update_record(obj)
        elif resolver == 'dnspod':
            api = RecordModify(obj)
            ret = api()
            code = ret.get("status", {}).get("code")
            if code == "1":
                record = ret.get("record", {})
                record_id = record.get("id")
                return {'code':1, "message":{'RecordId':record_id}}
            else:
                return {'code':0,'message':ret.get("status", {}).get("message")}

    def record_status(self, obj):
        resolver = obj.domain_name.account.resolver
        if resolver == 'aliyun':
            return AliyunDomainName.set_record_status(obj)
        elif resolver == 'dnspod':
            api = RecordStatus(obj)
            ret = api()
            code = ret.get("status", {}).get("code")
            if code == "1":
                record = ret.get("record", {})
                record_id = record.get("id")
                return {'code':1, "message":{'RecordId':record_id}}
            else:
                return {'code':0,'message':ret.get("status", {}).get("message")}

    def record_remove(self, obj):
        resolver = obj.domain_name.account.resolver
        if resolver == 'aliyun':
            return AliyunDomainName.del_record(obj)
        elif resolver == 'dnspod':
            api = RecordRemove(obj=obj)
            ret = api()
            code = ret.get("status", {}).get("code")
            if code == "1":
                record = ret.get("record", {})
                record_id = record.get("id")
                return {'code':1, "message":{'RecordId':record_id}}
            else:
                return {'code':0,'message':ret.get("status", {}).get("message")}

if __name__ == '__main__':
    pass