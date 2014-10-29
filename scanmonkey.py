#!/usr/bin/python

from pymongo import MongoClient
import nmap
import time
from random import randint

def scanHosts(hostList,runTime,dbName,monkeyId):
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
    
def saveResults(target,openPorts,dbName,startTime,endTime): 
    conn = MongoClient('127.0.0.1',27017) #default mongoDB security for PoC
    data = {'ip':target,'ports':openPorts}
    db = conn[dbName]
    hosts = db.hosts
    action = db.action
    
    if hosts.find({'ip' : target}).count() == 0:  #If the IP already exists in the database skip recording duplicate data
        hosts.insert(data)
    
    action.insert({'action':'synscan','ip':target,'start':startTime,'end':endTime}) #Record all monkey activity, even if it's already occurred (i.e.Same target gets hit more than once)
    
    