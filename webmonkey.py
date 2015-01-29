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


def findWebBoxes (runTime,dbIp,dbName,monkeyIq,monkeyLoc,monkeyId):
    timeout = time.time() + 60 * runTime

    while True:
        targets = [] #reinit variables each time through to account for new scanner data
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
                    if 80 in work['ports']:
                        targets.append(work['ip'])
                        ports.append(80)

                    elif 443 in work['ports']:
                        targets.append(work['ip'])
                        ports.append(443)

                else:
                    continue

        if len(targets) == 0:
            print 'Web monkey is waiting for a web server.  Eating bananas.  Will check again in 10 seconds.'
            time.sleep(10)

        else:
            print 'Web monkey got work! Starting directory brute forcing!'
            webBrute (targets,ports,db,hosts,monkeyId)

def webBrute(targets,ports,db,coll,monkeyId):
    index = randint(0,len(targets)-1)
    webIP = targets[index]
    webPort = ports[index]

    startTime = time.ctime()

    with open('./lists/weblist.txt') as f:
        for directory in f:
            if webPort == 80:
                try:
                    urllib2.urlopen('http://' + webIP + '/' + directory + '/', timeout=3 )

                except urllib2.URLError:
                    pass

            elif webPort == 443:
                try:
                    urllib2.urlopen('https://' + webIP + '/' + directory + '/',timeout=3 )

                except urllib2.URLError:
                    pass

    endTime = time.ctime()
    print 'finished directory brute forcing of ' + webIP + 'at ' + endTime
    saveResults(db,coll,webIP,webPort,startTime,endTime,monkeyId)

    return


def saveResults(dbConn,coll,target,port,startTime,endTime,monkeyId):
    action = dbConn.actions
    action.insert({'action':'webdirscan','ip':target,'port':port,'start':startTime,'end':endTime,'id':monkeyId})