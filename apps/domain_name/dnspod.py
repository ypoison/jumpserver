  #!/usr/bin/env python
# -*- coding:utf-8 -*-


import re
import requests
try:
    import json
except Exception:
    import simplejson as json

class ApiCn:
    def __init__(self, obj=None, login_token=None, **kw):
        self.base_url = "dnsapi.cn"
        if login_token:
            self.params = dict(
                login_token=login_token,
                format="json",
            )
        elif obj:
            try:
                self.params = dict(
                    login_token='%s,%s' % (obj.account.access_id,obj.account.access_key),
                    format="json",
                )
            except:
                                self.params = dict(
                    login_token='%s,%s' % (obj.domain_name.account.access_id,
                                           obj.domain_name.account.access_key),
                    format="json",
                )
        
        self.params.update(kw)
        self.path = None
    def request(self, **kw):
        self.params.update(kw)
        if not self.path:
            """Class UserInfo will auto request path /User.Info."""
            name = re.sub(r'([A-Z])', r'.\1', self.__class__.__name__)
            self.path = "/" + name[1:]
        headers = {
            "Content-type": "application/x-www-form-urlencoded",
            "Accept": "text/json",
            "User-Agent": "dnspod-python/0.01 (im@chuangbo.li; DNSPod.CN API v2.8)"
        }
        url = "https://" + self.base_url + self.path
        response = requests.post(url, data=self.params, headers=headers)
        data = response.text
        ret = json.loads(data)
        return ret

    __call__ = request


class DomainCreate(ApiCn):
    def __init__(self, obj, **kw):
        kw.update(dict(domain=obj.domain_name))
        ApiCn.__init__(self,obj=obj, **kw)


class DomainList(ApiCn):
    def __init__(self, obj, **kw):
        login_token='%s,%s' % (obj.access_id,obj.access_key),
        ApiCn.__init__(self, login_token=login_token, **kw)


class _DomainApiBase(ApiCn):
    def __init__(self, obj, **kw):
        kw.update(dict(domain=obj.domain_name))
        ApiCn.__init__(self, obj=obj, **kw)


class DomainRemove(_DomainApiBase):
    pass


class RecordList(_DomainApiBase):
    pass

class _RecordBase(ApiCn):
    def __init__(self, obj, **kw):
        kw.update(dict(
                    record_id=obj.record_id,
                    domain=obj.domain_name.domain_name
                    )
                )
        ApiCn.__init__(self, obj=obj, **kw)

class RecordCreate(_RecordBase):
    def __init__(self, obj, **kw):
        kw.update(dict(
            sub_domain=obj.rr,
            record_type=obj.type,
            record_line=obj.get_line_display().encode("utf8"),
            value=obj.value,
            ttl=obj.ttl,
        ))
        _RecordBase.__init__(self, obj=obj, **kw)


class RecordModify(RecordCreate):
    def __init__(self, obj, **kw):
        RecordCreate.__init__(self, obj, **kw)

class RecordRemove(_RecordBase):
    pass


class RecordDdns(_DomainApiBase):
    def __init__(self, record_id, sub_domain, record_line, **kw):
        kw.update(dict(
            record_id=record_id,
            sub_domain=sub_domain,
            record_line=record_line,
        ))
        _DomainApiBase.__init__(self, **kw)


class RecordStatus(_RecordBase):
    def __init__(self, obj, **kw):
        kw.update(dict(status=obj.status.lower()))
        _RecordBase.__init__(self, obj, **kw)


class RecordInfo(_RecordBase):
    pass