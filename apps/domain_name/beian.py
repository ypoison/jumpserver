#!/usr/bin/env python
# -*- coding:utf-8 -*-


import re
import requests
try:
    import json
except Exception:
    import simplejson as json

class beian:
    def __init__(self):
        self.headers = {
        "Content-type": "application/x-www-form-urlencoded",
        "Accept": "text/json",
        "User-Agent": "beian-python/0.01"
    }

    def check_beian(self,domain_name):
        url = "https://www.sojson.com/api/beian/%s" % domain_name
        try:
            response = requests.get(url,headers=self.headers)
            data = response.text
            ret = json.loads(data)
            if ret.get('type') == 200:
                return {'code':1}    
            else:
                return {'code':0}
        except:
            return {'code':0}

    def check_beian_slow(self,domain_name):
        appkey = '43430'
        sign = 'f44167febb3e9213c87eb315c080f82c'
        url = 'https://sapi.k780.com/?app=domain.beian \
                &domain=%s&appkey=%s&sign=%s&format=json' % (domain_name,appkey,sign)
        try:
            response = requests.get(url,headers=self.headers)
            data = response.text
            ret = json.loads(data)
            result = ret.get('result')
            if result:
                status = result.get('status')
                if status == 'ALREADY_BEIAN':
                    return {'code':1}
                elif status == 'WAIT_PROCESS':
                    return {'code':2}
                else:
                    return {'code':0}
            else:
                return {'code':-1, 'msg':ret.get('msg')}
        except:
            return {'code':-1, 'msg':'接口调用出错'}

if __name__ == '__main__':
    beian = beian()
    print(beian.check_beian('baidu.com'))