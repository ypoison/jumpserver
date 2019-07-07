#!/usr/bin/env python
import requests
import json

headers = { "Authorization": "Token 1287b4dff75fe35afbf86aa49098a84ec1573849" }
url = "http://localhost/api/domain-name/v1/domain-name-records/"
query_args = {
            'domain_name':'shuishequ.cn',
            'type':'A',
            'rr':'test',
            'line':'default',
            'value':'192.168.1.100'
                                }
response = requests.post(url, data=query_args, headers=headers)
data = response.text
#ret = json.loads(data)
print(data)
