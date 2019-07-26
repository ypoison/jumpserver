#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author:Matt Hsu
# date :2019/07/24

from ucloud.core import exc
from ucloud.client import Client

import hashlib
import requests
import json
import operator

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
            project_list = []
            for p in ret['ProjectSet']:
                project_list.append({'id':p['ProjectId'],'name':p['ProjectName'],'IsDefault':p['IsDefault']})
            return {'code':1, 'msg':project_list}
        else:
            return {'code':0, 'msg':ret['Message']}

    def GetRegion(self, **kwargs):
        kwargs['Action'] = 'GetRegion'
        ret = self.response(**kwargs)
        if ret.get('RetCode', '') == 0:
            region_list = []
            for r in ret['Regions']:
                region = {'IsDefault':r['IsDefault'],'id':r['Region'],'name':r['Region']}
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
                    zone = {'Region':z['Region'], 'name':z['Zone'],'id':z['Zone']}
                    zone_list.append(zone)
            return {'code':1, 'msg':zone_list}
        else:
            return {'code':0, 'msg':ret['Message']}

    def GetImageList(self, **kwargs):
        kwargs['Action'] = 'DescribeImage'
        ret = self.response(**kwargs)
        if ret.get('RetCode', '') == 0:
            image_list = []
            for i in ret['ImageSet']:
                image_list.append({'id':i['ImageId'], 'name':i['ImageName']})
            if image_list:
                image_list = sorted(image_list, key=operator.itemgetter('name'))
            return {'code': 1, 'msg': image_list}
        else:
            return {'code': 0, 'msg': ret['Message']}

    def GetVPC(self, **kwargs):
        kwargs['Action'] = 'DescribeVPC'
        ret = self.response(**kwargs)
        if ret.get('RetCode', '') == 0:
            vpc_list = []
            for v in ret['DataSet']:
                vpc = { 'name':v['Name'],'id':v['VPCId']}
                vpc_list.append(vpc)
            return {'code': 1, 'msg': vpc_list}
        else:
            return {'code': 0, 'msg': ret['Message']}

    def GetSubnet(self, **kwargs):
        vpc_id = kwargs.pop('vpc_id')
        kwargs['Action'] = 'DescribeSubnet'
        ret = self.response(**kwargs)
        if ret.get('RetCode', '') == 0:
            subnet_list = []
            for s in ret['DataSet']:
                if s['VPCId'] == vpc_id:
                    subnet = { 'name':s['Subnet'],'id':s['SubnetId']}
                    subnet_list.append(subnet)
            return {'code': 1, 'msg': subnet_list}
        else:
            return {'code': 0, 'msg': ret['Message']}


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