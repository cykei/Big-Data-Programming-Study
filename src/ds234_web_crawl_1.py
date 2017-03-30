# coding: utf-8
import requests
import re
rsp = requests.get('http://python.org/')
tempHTML= rsp.text

#p=re.compile('http://.+"')
p=re.compile('href="(http://.*?)"')
nodes=p.findall(tempHTML)
for i, node in enumerate(nodes):
    print i, node