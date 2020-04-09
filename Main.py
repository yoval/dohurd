# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 10:56:42 2020

@author: Fuwenyue
"""


import requests,time

proxies = {
  'http': 'socks5://127.0.0.1:10808',
  'https': 'socks5://127.0.0.1:10808',
}
URL = 'http://dohurd.ah.gov.cn/epoint-mini/rest/function/searchSNQY?IsAjax=1&dataType=json&_=0.9331907955118341'
data = {
    'pagesize': 1069,
    'pageindex': 1,
    'type': 2,
    'CorpCode': '',
    'CorpName': '',
    'LegalMan': '',
    'CertTypeNum': '',
    'txt1':'' ,
    'AreaCode': 3404}

Req= requests.post(URL,data)
Json = Req.json()
HuaiNanList = Json['all']['listinfo']
#无证书解析
def jiexi0(LegalMan,CorpName,AreaCode):
    with open('HuaiNan.csv','a',) as f:
        f.writelines([LegalMan,',',CorpName,',',AreaCode,',','无有效证书','\n'])
#一个证书解析
def jiexi1(REq):
    REqList = REq['all']['listinfo'][0]
    endate = REqList['enddate']
    organname = REqList['organname']
    if organname :
        pass
    else:
        organname = organname
    certname = REqList['certname']
    with open('HuaiNan.csv','a',) as f:
        f.writelines([LegalMan,',',CorpName,',',AreaCode,',',certname,',',organname,',',endate,'\n'])
#多证书解析
def jiexi2(REq):
    REqList = REq['all']['listinfo']
    for REqList in REqList:
        endate = REqList['enddate']
        organname = REqList['organname']
        if organname:
            pass
        else:
            organname = 'organname'
        certname = REqList['certname']
        with open('HuaiNan.csv','a',) as f:
            f.writelines([LegalMan,',',CorpName,',',AreaCode,',',certname,',',organname,',',endate,'\n'])
for huainan in HuaiNanList:
    time.sleep(5)
    LegalMan = huainan['legalman']
    CorpName = huainan['corpname']
    AreaCode = huainan['areacodetext']
    CorpCode = huainan['corpcode']
    Rowguid = huainan['rowguid']

    U = 'http://dohurd.ah.gov.cn/epoint-mini/rest/function/searchQYXQ'
    Data = {
        'pagesize': 12,
        'pageindex': 1,
        'PageType':'' ,
        'corpcode': CorpCode}
    try:
        REq = requests.post(U,Data)
        REq = REq.json()
    except:
        print('用代理尝试……')
        REq = requests.post(U,Data,proxies=proxies)
        REq = REq.json()        
    total8 = REq['all']['total']
    if total8 ==0:
        jiexi0(LegalMan,CorpName,AreaCode)
    elif total8 ==1:
        jiexi1(REq)
    elif total8>1:
        jiexi2(REq)

