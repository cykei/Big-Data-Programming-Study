# coding: utf-8
import lxml.html
from lxml.cssselect import CSSSelector
import requests
r = requests.get('http://www.ieee.org/conferences_events/conferences/search/index.html')

html = lxml.html.fromstring(r.text)
sel=CSSSelector('div.content-r-full table.nogrid-nopad tr p>a[href]')
nodes = sel(html)
for node in nodes:
    print node.text
    print "----------"