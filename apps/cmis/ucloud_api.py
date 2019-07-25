#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author:Matt Hsu
# date :2019/07/24

from ucloud.core import exc
from ucloud.client import Client

import hashlib
import requests
import json
class UcloudAPI:
    def __init__(self):
        self.url = 'https://api.ucloud.cn'
    def _verfy_ac(self, private_key, params):
        items = list(params.items())
        items.sort()
        params_data = ""
        for key, value in items:
            params_data = params_data + str(key) + str(value)
        params_data = params_data + private_key
        sign = hashlib.sha1()
        sign.update(params_data.encode("utf8"))
        signature = sign.hexdigest()
        return signature

    def response(self, **kwargs):
        private_key = kwargs.pop('PrivateKey')
        signature = self._verfy_ac(private_key, kwargs)
        kwargs['Signature'] = signature
        res = requests.post(self.url, data=kwargs)
        content = res._content
        ret = json.loads(content)
        return ret
    def GetProjectList(self, **kwargs):
        kwargs['Action'] = 'GetProjectList'
        ret = self.response(**kwargs)
        if ret.get('RetCode', '') == 0:
            return {'code':1, 'msg':ret['ProjectSet']}
        else:
            return {'code':ret['RetCode'], 'msg':ret['Message']}

    def GetRegion(self, **kwargs):
        kwargs['Action'] = 'GetRegion'
        ret = self.response(**kwargs)
        if ret.get('RetCode', '') == 0:
            region_list = []
            for r in ret['Regions']:
                region = {'IsDefault':r['IsDefault'],'Region':r['Region']}
                if region not in region_list:
                    region_list.append(region)
            return {'code':1, 'msg':region_list}
        else:
            return {'code':0, 'msg':ret['Message']}

    def GetZone(self, **kwargs):
        kwargs['Action'] = 'GetRegion'
        region = kwargs.pop('Region')
        ret = self.response(**kwargs)
        if ret.get('RetCode', '') == 0:
            zone_list = []
            for z in ret['Regions']:
                if z['Region'] == region:
                    zone = {'Region':z['Region'], 'Zone':z['Zone']}
                    zone_list.append(zone)
            return {'code':1, 'msg':zone_list}
        else:
            return {'code':0, 'msg':ret['Message']}

    def GetImageList(self, **kwargs):
        client = Client({
            "region": kwargs.pop('Region'),
            "project_id": kwargs.pop('project_id'),
            "public_key": kwargs.pop('PublicKey'),
            "private_key": kwargs.pop('PrivateKey'),
        })

        try:
            resp = client.uhost().describe_image(kwargs)
        except exc.UCloudException as e:
            return {'code':0, 'msg':e}
        else:
            return {'code':1, 'msg':resp['ImageSet']}

def CreateUhostInstance(**kwargs):
    client = Client({
        "region": "cn-bj2",
        "project_id": "org-mdspst",
        "public_key": "uikwBtgRRKbTyBh6WGZVH9oqLf7VGZMgJbVALie/y4sxhUVoFV4ktA==",
        "private_key": "u5IOOxOwQSFib5deoSdGxvKm5INFInDeKpmv+e+adexx4/2MTRqC8WXV8iKaWh0Y",
    })

    try:
        resp = client.uhost().create_uhost_instance({
            'Name': 'sdk-python-quickstart',
            'Zone': 'cn-bj2-04',
            'ImageId': 'uimage-y0kl0s',
            'LoginMode': "Password",
            'Password': 'UGFzc3dvcmQx',
            'CPU': 1,
            'Memory': 1024,
            'Disks': [{
                'Size': 30,
                'Type': 'CLOUD_SSD',
                'IsBoot': True,
            }],
        })
    except exc.UCloudException as e:
        print(e)
    else:
        print(resp)

if __name__ == '__main__':
    data = {
        'PrivateKey' : 'u5IOOxOwQSFib5deoSdGxvKm5INFInDeKpmv+e+adexx4/2MTRqC8WXV8iKaWh0Y',
        "Action": "GetRegion",
        #"Action": "GetProjectList",
        "PublicKey": "uikwBtgRRKbTyBh6WGZVH9oqLf7VGZMgJbVALie/y4sxhUVoFV4ktA==",
    }
    api = UcloudAPI()
    #print(api.GetProjectList(**data))
    print(DescribeImage())