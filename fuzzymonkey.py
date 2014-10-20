#!/usr/bin/python
from socket import *
from pymongo import MongoClient
from random import randint
from random import choice
from sys import getsizeof
import time
import string



def fuzzPorts(runTime,dbName):
    timeout = time.time() + 60 * runTime
    conn = MongoClient('127.0.0.1',27017)
    db = conn[dbName]
    hosts = db.hosts
    
    while True:
        targets = [] #reinit each time through
        time.sleep(1)
        
        if time.time() > timeout:
            break
        
        start = time.ctime()
        
        if hosts.find().count() == 0:
            print 'Fuzzy monkey is waiting for work.  Eating bananas.  Will check again in 10 seconds.'
            time.sleep(10)
        
        else:
            for work in hosts.find():
                targets.append(work)

            index = randint(0,len(targets)-1)
            fuzzIP = str(targets[index]['ip'])
            fuzzTCP = str(targets[index]['ports'][randint(0,len(targets[index]['ports'])-1)])
            fuzzData = genFuzzData(randInt(1,100000))
            print 'Fuzzy monkey got work! Fuzzing ' + fuzzIP + 'on port ' + fuzzTCP + 'with ' + str(sys.getsizeof(fuzzData)) + 'bytes of data!'
            
            s = socket(AF_INET, SOCK_STREAM)
            s.connect((fuzzIP, fuzzTCP))
            s.send(fuzzData)
            s.close()

def genFuzzData(fuzzLen):
        return ''.join(choice(string.ascii_letters + string.digits +'!@#$%^&*()' for x in range(fuzzLen) ))