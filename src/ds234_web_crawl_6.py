# coding: utf-8
import requests
import lxml.etree

def getBaseballData():
    req = requests.get('http://www.kbreport.com/main')
    _htmlTree = lxml.etree.HTML(req.text)
    nodes = _htmlTree.xpath("//div[@class='team-rank-box']//table[@class='team-rank']//tr")
    print u"테이블 행 갯수: ", len(nodes)
    counter=0
    for teams in nodes:
        for cols in teams:
            if cols.xpath('.//a/text()'):
                print cols.xpath('.//a/text()')[0],
            else:
                print cols.text.strip(),
        print

def main():
    getBaseballData()

if __name__ == "__main__":
    main()
