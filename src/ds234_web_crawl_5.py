# coding: utf-8
import lxml.html
from lxml.cssselect import CSSSelector
import requests
req = requests.get('http://www.ieee.org/conferences_events/conferences/search/index.html')

html = lxml.html.fromstring(req.text)

cssSel=CSSSelector('div.content-r-full table.nogrid-nopad tr p>a[href]')
nodes = cssSel(html)

print "학회목록"
for node in nodes:
        print node.text
        print "----------------"
    
    