#!/usr/bin/env python
import requests
import json
class WEBConfig:
        def __init__(self):
            self.headers = { "Content-Type": "application/json" }
        def add(self,**kwargs):
            node_ip = kwargs['node_ip']
            url = 'http://%s:10125/webconf/api/v1.0/add' % (node_ip)
            query_args = {
                 'domain':kwargs['domain'],
                  'port':kwargs['port'],
                  'platform':kwargs['platform'],
                  'proxyip':kwargs['proxy_ip'],
                  'proxyport':kwargs['proxy_port'],
                  'notes':kwargs['comment'],
                  }
            try:
                dresponse = requests.post(url, data=json.dumps(query_args), headers=self.headers)
                if dresponse.status_code == 200:
                    data = json.loads(dresponse.text)
                    if data['status'] == 2000:
                        ret = {'code':1}
                    else:
                        ret = {'code':0, 'msg':data['resultInfo']}
                else:
                    ret = {'code': 0, 'msg': '调用接口失败:status_code:%s' % dresponse.status_code}
            except Exception as e:
                ret = {'code':0, 'msg':'调用接口失败:%s' % e}
            return  ret

        def remove(self,**kwargs):
            node_ip = kwargs['node_ip']
            url = 'http://%s:10125/webconf/api/v1.0/del' % (node_ip)
            query_args = {
                'domain':kwargs['domain'],
                'platform':kwargs['platform']
            }
            try:
                dresponse = requests.post(url, data=json.dumps(query_args), headers=self.headers)
                if dresponse.status_code == 200:
                    data = json.loads(dresponse.text)
                    if data['status'] == 2000:
                        ret = {'code':1}
                    else:
                        ret = {'code':0, 'msg':data['resultInfo']}
                else:
                    ret = {'code': 0, 'msg': '调用接口失败:status_code:%s' % dresponse.status_code}
            except Exception as e:
                ret = {'code':0, 'msg':'调用接口失败%s' % e}
            return  ret

        def reload(self,**kwargs):
            node_ip = kwargs['node']
            url = 'http://%s:10125/webconf/api/v1.0/reload' % (node_ip)
            query_args = {
                'nodeip': node_ip,
            }
            try:
                dresponse = requests.post(url, data=json.dumps(query_args), headers=self.headers)
                if dresponse.status_code == 200:
                    data = json.loads(dresponse.text)
                    if data['status'] == 2000:
                        ret = {'code': 1}
                    else:
                        ret = {'code': 0, 'msg': data['resultInfo']}
                else:
                    ret = {'code': 0, 'msg': '调用接口失败:status_code:%s' % dresponse.status_code}
            except Exception as e:
                ret = {'code': 0, 'msg': '调用接口失败%s' % e}
            return ret
if __name__ == '__main__':
    webconfig = WEBConfig()
    kwargs = {'_state': '<django.db.models.base.ModelState object at 0x7fb29170c400>',
            'id': 'UUID(80a4860b-875b-4205-b49c-41931388ecbd)',
                'platform_id': 'UUID(47374616-c07c-485c-8608-8dcde2f9add9)',
    'domain': 'api.pppxia.com', 'port': 1231, 'proxy_ip': '3.3.3.3', 'proxy_port': 123, 'comment': '', 'platform': 'DY','public_node_ip':'192.168.1.124'}

    print(webconfig.add(**kwargs))
