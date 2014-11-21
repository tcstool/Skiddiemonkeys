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

def scanHosts(runTime,dbIp,dbName,monkeyIq):
    timeout = time.time() + 60 * runTime
    
    while True:
        time.sleep(1)

        openPorts = [] #reinit each time through loop
        if time.time() > timeout:
            break
        
        start = time.ctime()
        index = randint(0,len(hostList)-1)
        nm = nmap.PortScanner()
        nm.scan(hostList[index])
        end = time.ctime()
        print "Scan monkey finished scan of " + hostList[index] + " at " + end
        
        if len( nm.all_hosts() ) != 0:
            for port in nm[nm.all_hosts()[0]]['tcp'].keys():
                if nm[nm.all_hosts()[0]]['tcp'][port]['state'] == 'open':
                    openPorts.append(port)
             
            if len(openPorts) != 0:        
                saveResults(nm.all_hosts()[0],openPorts,dbName,start,end)
    
def saveResults(target,openPorts,dbIp,dbName,startTime,endTime):
    conn = MongoClient(dbIp,27017) #default mongoDB security for PoC
    data = {'ip':target,'ports':openPorts}
    db = conn[dbName]
    hosts = db.hosts
    action = db.action
    
    if hosts.find({'ip' : target}).count() == 0:  #If the IP already exists in the database skip recording duplicate data
        hosts.insert(data)
    
    action.insert({'action':'synscan','ip':target,'start':startTime,'end':endTime}) #Record all monkey activity, even if it's already occurred (i.e.Same target gets hit more than once)
    
    