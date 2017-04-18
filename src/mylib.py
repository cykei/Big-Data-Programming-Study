def sayHello():
    print "hello"
def sayHello2():
    print "hello2"
def getKey(keyPath):
    d=dict()
    f=open(keyPath,'r')
    for line in f.readlines():
        row=line.split('=')
        key=row[0]
        d[key]=row[1].strip()
    return d