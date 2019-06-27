#!/usr/bin/env python
# -*- coding:utf-8 -*-


import dnspod


def main():
    # please refer to:
    # https://support.dnspod.cn/Kb/showarticle/tsid/227/
    login_token = "101760,83080961c3dd8cd59eb5298729577a6e"

    domain = "Your DOMAIN here"

    #print "DomainCreate", domain
    #api = apicn.DomainCreate(domain, login_token=login_token)
#
    #domain_id = api().get("domain", {}).get("id")
    #print "%s's id is %s" % (domain, domain_id)

    #print("DomainList")
    #api = dnspod.DomainList(login_token=login_token)
    #print(api().get("domains"))

    #print "RecordType"
    #api = apicn.RecordType("D_Ultra", login_token=login_token)
    #print api().get("types")
#
    #print "RecordLine"
    #api = apicn.RecordLine("D_Free", login_token=login_token)
    #print api().get("lines")
#
    #print "RecordCreate"
    #api = apicn.RecordCreate("www", "A", u'默认'.encode("utf8"), '1.1.1.1', 600, domain_id=domain_id, login_token=login_token)
    #record = api().get("record", {})
    #record_id = record.get("id")
    #print "Record id", record_id
#
    print("RecordList")
    api = dnspod.RecordList('wlqp.in', login_token=login_token)
    print(api().get("records"))
#
    #print "DomainRemove"
    #api = apicn.DomainRemove(domain_id, login_token=login_token)
    #print api()

class A:
    def __init__(self):
        print('A')
class B(A):
    def __init__(self,d):
        b=d
        print('B')
class C(B):
    def __init__(self,d):
        print('C')


if __name__ == '__main__':
    #main()
    a=C('dddd')
    print(a)