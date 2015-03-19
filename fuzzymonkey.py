#!/usr/bin/python
#Skiddemonkeys Copyright 2014 Russell Butturini
#This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.
from socket import *
from pymongo import MongoClient
from random import randint
from random import choice
from sys import getsizeof
import time
import string



def fuzzPorts(runTime,dbIp,dbName,monkeyIq,monkeyLoc,minData,maxData,monkeyId):
    timeout = time.time() + 60 * runTime

    while True:
        hostList = {} #reinit each time through
        time.sleep(1)

        
        if time.time() > timeout:
            break

        conn = MongoClient(dbIp,27017)
        db = conn[dbName]
        hosts = db.hosts
        
        if hosts.find({'location':monkeyLoc}).count() == 0:
            print 'Fuzzy monkey is waiting for work.  Eating bananas.  Will check again in 10 seconds.'
            time.sleep(10)
        
        else:
            for work in hosts.find({'location':monkeyLoc}):
                #Start priority calculation
                decisionCalc = ( int(monkeyIq) * int(db.targets.find_one({'ip' : work['ip']})['value']))/(db.actions.find({'ip' : work['ip'] }).count() + 1 ) + randint(1,10)
                hostList.update( {work['ip'] : decisionCalc } )

            target = max(hostList,key=hostList.get)
            openPorts = db.hosts.find_one({'ip' : target})['ports']
            fuzzTCP = openPorts[randint(0,len(openPorts)-1)]
            fuzzData = genFuzzData(randint(int(minData),int(maxData)))
            print 'Fuzzy monkey got work! Fuzzing ' + target + ' on port ' + str(fuzzTCP) + ' with ' + str(getsizeof(fuzzData)) + ' bytes of data!'
            
            start = time.ctime()


            try:
                s = socket(AF_INET, SOCK_STREAM)
                s.settimeout(10)
                s.connect((target, fuzzTCP))
                s.send(fuzzData)
                result = s.recv(100) #Don't care what we get back.
                s.close()

            except:
                #Handle TCP resets and other aggressive network traffic semi gracefully
                pass

            end = time.ctime()
            saveResults(db,hosts,target,fuzzTCP,str(getsizeof(fuzzData)),start,end,monkeyId)
            print 'Fuzzy monkey need sleep.  Resting for 5 seconds.'
            time.sleep(5)

def saveResults(dbConn,coll,target,port,size,startTime,endTime,monkeyId):
    action = dbConn.actions
    action.insert({'action':'fuzz','ip':target,'port':port,'bytes':size,'start':startTime,'end':endTime,'id':monkeyId})
    
    

def genFuzzData(fuzzLen):
        return ''.join(choice(string.ascii_letters + string.digits +'!@#$%^&*()') for x in range(fuzzLen) )