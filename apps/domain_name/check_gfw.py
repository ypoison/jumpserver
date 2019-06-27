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
        self.headers = {
        "Content-type": "application/json; charset=UTF-8",
        "accept": "application/json, text/javascript, */*; q=0.01",
        "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"
    }
        self.params = dict(
                func = 'true',
                m = 'check',
                a = 'check',
                domain = 'google.com',
                x_post_with = 'fcm-ajax',
        )

    def check_gfw(self,domain_name):
        url = 'https://www.checkgfw.com/service.cgi/check'
        #try:
        response = requests.post(url,data=self.params, headers=self.headers)
        data = response.text
        ret = json.loads(data)
        return ret
        #    result = ret.get('result')
        #    if result:
        #        status = result.get('status')
        #        if status == 'ALREADY_BEIAN':
        #            return {'code':1}
        #        elif status == 'WAIT_PROCESS':
        #            return {'code':2}
        #        else:
        #            return {'code':0}
        #    else:
        #        return {'code':-1, 'msg':ret.get('msg')}
        #except:
        #    return {'code':-1, 'msg':'接口调用出错'}

if __name__ == '__main__':
    check = CheckGFW()
    print(check.check_gfw('baidu.com'))