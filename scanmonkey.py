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
import nmap
import time
from random import randint

def scanHosts(runTime,dbIp,dbName,monkeyIq,monkeyLoc,monkeyId):
    timeout = time.time() + 60 * runTime
    
    while True:
        time.sleep(1)

        hostList = {} #reinit each time through loop to get new hosts from other clients possibly.
        openPorts = [] #reinit each time through loop

        if time.time() > timeout:
            break

        conn = MongoClient(dbIp,27017)
        db = conn[dbName]

        for host in db.targets.find({'location':monkeyLoc}):
            #Start priority calculation
            decisionCalc = ( int(monkeyIq) * int(host['value']) )/(db.actions.find({'ip' : host }).count() + 1 ) + randint(1,10)
            hostList.update( {host['ip'] : decisionCalc } )

        print str(hostList) #debug
        #Find highest decision calculation
        target = max(hostList,key=hostList.get)

        start = time.ctime()
        #index = randint(0,len(hostList)-1)
        print 'Starting port scan of ' + target
        nm = nmap.PortScanner()

        if int(monkeyIq) == 0: #Almost as smart as Gregory Evans
            nm.scan(target)

        elif int(monkeyIq) == 1: #Level 1 monkeys aren't foiled by ICMP being blocked to the host
            nm.scan(target,arguments='-P0 -A')

        elif int(monkeyIq) == 2: #Level 2 monkeys run full connect scans to be a bit more stealthy
            nm.scan(target,arguments='-P0 -sT -A')

        elif int(monkeyIq) == 3: #Level 3 monkeys include decoy IPs in their scans
            nm.scan(target,arguments='-P0,-sT,-A,-D4.2.2.2,8.8.8.8,172.1.2.4,3.4.2.1')

        end = time.ctime()
        print "Scan monkey finished scan of " + target + " at " + end
        
        if len( nm.all_hosts() ) != 0:
            for port in nm[nm.all_hosts()[0]]['tcp'].keys():
                if nm[nm.all_hosts()[0]]['tcp'][port]['state'] == 'open':
                    openPorts.append(port)
             
            if len(openPorts) != 0:        
                saveResults(nm.all_hosts()[0],openPorts,dbName,start,end,conn,monkeyId,monkeyLoc)

    print 'Monkey shift is over.'
    return
    
def saveResults(target,openPorts,dbName,startTime,endTime,conn,monkeyId,location):
    db = conn[dbName]
    data = {'ip':target,'ports':openPorts, 'location':location}
    hosts = db.hosts
    action = db.actions
    
    if hosts.find({'ip' : target}).count() == 0:  #If the IP already exists in the database skip recording duplicate data
        hosts.insert(data)
    
    action.insert({'action':'synscan','ip':target,'start':startTime,'end':endTime,'id':monkeyId}) #Record all monkey activity, even if it's already occurred (i.e.Same target gets hit more than once)
    