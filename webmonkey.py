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

from pymongo import MongoClient
from random import randint
import time
import urllib2
import ssl

def findWebBoxes (runTime,dbIp,dbName,monkeyIq,monkeyLoc,monkeyId):
    timeout = time.time() + 60 * runTime

    while True:
        hostList = {} #reinit variables each time through to account for new scanner data
        ports = []
        time.sleep(1)

        if time.time() > timeout:
            break

        conn = MongoClient(dbIp,27017)
        db = conn[dbName]
        hosts = db.hosts

        if hosts.find({'location':monkeyLoc}).count() == 0:
            print 'Web monkey is waiting for work.  Eating bananas.  Will check again in 10 seconds.'
            time.sleep(10)

        else:
            for work in hosts.find({'location':monkeyLoc}):
                if 80 in work['ports'] or 443 in work['ports']:
                    decisionCalc = ( int(monkeyIq) * int(db.targets.find_one({'ip' : work['ip']})['value']))/(db.actions.find({'ip' : work['ip'] }).count() + 1 ) + randint(1,10)
                    hostList.update( {work['ip'] : decisionCalc } )

            if len(hostList) > 0:
                target = max(hostList,key=hostList.get)
                openPorts = db.hosts.find_one({'ip' : target})['ports']

            if 80 in openPorts:
                ports.append(80)

            if 443 in openPorts:
                ports.append(443)

        if len(ports) == 0:
            print 'Web monkey is waiting for a web server.  Eating bananas.  Will check again in 10 seconds.'
            time.sleep(10)

        else:
            print 'Web monkey got work! Starting directory brute forcing!'
            index = randint(0,len(ports)-1)
            port = ports[index]
            webBrute (target,port,db,hosts,monkeyId)

def webBrute(target,port,db,coll,monkeyId):

    startTime = time.ctime()

    try:
        with open('./lists/weblist.txt') as f:
            dirList = f.readlines()

    except:
        print 'Error:  Couldn\'t open directory brute forcing file.'
        return


    for directory in dirList:
        if port == 80:
            try:
                urllib2.urlopen('http://' + target + '/' + directory.rstrip() + '/', timeout=3 )

            except urllib2.URLError:
                pass

            except ssl.SSLError:
                pass

        elif port == 443:
            try:
                urllib2.urlopen('https://' + target + '/' + directory.rstrip() + '/',timeout=3 )

            except urllib2.URLError:
                pass

            except ssl.SSLError:
                pass

    endTime = time.ctime()
    print 'finished directory brute forcing of ' + target + ' at ' + endTime
    saveResults(db,coll,target,port,startTime,endTime,monkeyId)

    return


def saveResults(dbConn,coll,target,port,startTime,endTime,monkeyId):
    action = dbConn.actions
    action.insert({'action':'webdirscan','ip':target,'port':port,'start':startTime,'end':endTime,'id':monkeyId})
    return