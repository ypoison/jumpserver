#!/usr/bin/env python
# -*- coding:utf-8 -*-


import re
import requests
try:
    import json
except Exception:
    import simplejson as json

class CheckGFW:
    def __init__(self):
        self.params = dict(
                func = 'true',
                m = 'check',
                a = 'check',
                x_post_with = 'fcm-ajax',
        )
    def check_gfw(self,domain_name):
        url = 'https://www.checkgfw.com/service.cgi/check'
        self.params.update(dict(domain=domain_name))
        try:
            response = requests.post(url, data=self.params)
            content = response._content
            ret = json.loads(content)
            data = response.text
            status = ret.get('type')
            if status:
                if status == 'success':
                    return {'code':1}
                else:
                    return {'code':0}
            else:
                return {'code':-1, 'msg':str(ret.get('msg'))}
        except Exception as e:
            return {'code':-1, 'msg':'check gfw 接口调用失败:%s' % e}

if __name__ == '__main__':
    check = CheckGFW()
    print(check.check_gfw('lfzgames.cn'))