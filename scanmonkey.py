#!/usr/bin/python

from pymongo import MongoClient
import nmap
import time
from random import randint

def scanHosts(hostList,runTime,dbName):
    timeout = time.time() + 60 * runTime
    
    while True:
        time.sleep(1)
        if time.time() > timeout:
            break
    
        index = randint(0,len(hostList)-1)
        nm = nmap.PortScanner()
        print hostList[index].rstrip() #debug

        if len( nm.all_hosts() ) != 0:
            print nm[hostList[index].rstrip()]['tcp'].keys() #debug
            saveResults(nm.all_hosts()[0],nm[nm.all_hosts()[0]]['tcp'].keys(),dbName)
        
    
    
def saveResults(target,openPorts,dbName): 
    conn = MongoClient('127.0.0.1',27017) #default mongoDB security for PoC
    data = {'ip':target,"ports":openPorts}
    db = conn[dbName]
    hosts = db.hosts
    
    if hosts.find({'ip' : target}).count() == 0:  #If the IP already exists in the database skip recording duplicate data
        hosts.insert(data)
    