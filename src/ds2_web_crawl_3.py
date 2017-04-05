# coding: utf-8
import re
from urllib import FancyURLopener
class MyOpener(FancyURLopener):
    version = 'My new User-Agent'
print MyOpener.version


class MyOpener(FancyURLopener):
    version = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:42.0) Gecko/20100101 Firefox/42.0'
print MyOpener.version

myopener = MyOpener()
page = myopener.open('http://www.google.com/search?q=python') #open의 의미는?
html=page.read()

p=re.compile('href="(https://.*?)"')
#p=re.compile('.*href.*')
res=p.findall(html)
print len(res)
for item in res:
    print item[:100]