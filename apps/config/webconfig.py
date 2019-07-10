#!/usr/bin/env python
import requests
import json
class WEBConfig:
        def __init__(self):
            self.headers = { "Content-Type": "application/json" }
            self.url = "http://192.168.1.171:10125/webconf/api/v1.0"
        def add(self,**kwargs):
            url = '%s/add' % (self.url)
            query_args = {
                 'domain':kwargs['domain'],
                  'port':kwargs['port'],
                  'platform':kwargs['platform'],
                  'proxyip':kwargs['proxyip'],
                  'proxyport':kwargs['proxyport']
                  }
            response = requests.post(url, data=json.dumps(query_args), headers=self.headers)
            data = response.text
            #ret = json.loads(data)
            return  data

        def remove(self,**kwargs):
            url = '%s/del' % (self.url)
            query_args = {
                'domain':kwargs['domain'],
                'platform':kwargs['platform']
            }
            response = requests.post(url, data=json.dumps(query_args), headers=self.headers)
            data = response.text
            # ret = json.loads(data)

            return data
if __name__ == '__main__':
    webconfig = WEBConfig()
    print(webconfig.add())