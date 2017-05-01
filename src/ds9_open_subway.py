#coding : utf-8
import os
import urlparse
import requests
import lxml
import lxml.etree
import StringIO
import mylib

def linenum(KEY,TYPE,SERVICE,START_INDEX,END_INDEX,LINE_NUM):
    params=KEY+'/'+TYPE+'/'+SERVICE+'/'+START_INDEX+'/'+END_INDEX+'/'+LINE_NUM
    print params[31:]

    _url='http://openAPI.seoul.go.kr:8088/'
    url=urlparse.urljoin(_url,params)
    data=requests.get(url).text
    tree=lxml.etree.fromstring(data.encode('utf-8'))
    nodes=tree.xpath('//STATION_NM')
    print 'line ',LINE_NUM,':'
    for node in nodes:
        print node.text,
def doIt():
    keyPath=os.path.join(os.getcwd(), 'src', 'key.properties')
    key=mylib.getKey(keyPath)
    KEY=str(key['dataseoul'])
    TYPE='xml'
    SERVICE='SearchSTNBySubwayLineService'
    START_INDEX=str(1)
    END_INDEX=str(10)
    for i in range(1,10):
        LINE_NUM=str(i)
        linenum(KEY,TYPE,SERVICE,START_INDEX,END_INDEX,LINE_NUM)

if __name__ == "__main__":
    doIt()