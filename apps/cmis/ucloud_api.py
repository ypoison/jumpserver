#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author:Matt Hsu
# date :2019/07/24

from ucloud.core import exc
from ucloud.client import Client

def GetProjectList(**kwargs):
    client = Client({
        "region": "cn-bj2",
        "project_id": "org-mdspst",
        "public_key": "uikwBtgRRKbTyBh6WGZVH9oqLf7VGZMgJbVALie/y4sxhUVoFV4ktA==",
        "private_key": "u5IOOxOwQSFib5deoSdGxvKm5INFInDeKpmv+e+adexx4/2MTRqC8WXV8iKaWh0Y",
    })

    try:
        resp = client.uhost().describe_image({
            'ImageType': 'Base',
            'Zone': 'cn-bj2-02',
            'OsType': 'Windows'
        })
    except exc.UCloudException as e:
        return e
    else:
        return resp

def DescribeImage(**kwargs):
    client = Client({
        "region": "cn-bj2",
        "project_id": "org-mdspst",
        "public_key": "uikwBtgRRKbTyBh6WGZVH9oqLf7VGZMgJbVALie/y4sxhUVoFV4ktA==",
        "private_key": "u5IOOxOwQSFib5deoSdGxvKm5INFInDeKpmv+e+adexx4/2MTRqC8WXV8iKaWh0Y",
    })

    try:
        resp = client.uhost().describe_image({
            'ImageType': 'Base',
            'Zone': 'cn-bj2-02',
            'OsType': 'Windows'
        })
    except exc.UCloudException as e:
        return e
    else:
        return resp

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

    CreateUhostInstance()