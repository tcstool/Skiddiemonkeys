#!/usr/bin/python

import paramiko
import ftplib
import telnetlib
import socket
import time
from pymongo import MongoClient
from random import randint

def findLoginBoxes(runTime,dbIp,dbName,monkeyIq,monkeyLoc,monkeyId):
    timeout = time.time() + 60 * runTime

    while True:
        targets = []
        ports = []
        time.sleep(1)

        if time.time() > timeout:
            break

        conn = MongoClient(dbIp,27017)
        db = conn[dbName]
        hosts = db.hosts


        if hosts.find({'location':monkeyLoc}).count() == 0:
            print 'Brute monkey is waiting for work.  Eating bananas.  Will check again in 10 seconds.'
            time.sleep(10)

        else:
            for work in hosts.find({'location':monkeyLoc}):
                if 21 in work['ports']:
                    targets.append(work['ip'])
                    ports.append(21)

                if 22 in work['ports']:
                    targets.append(work['ip'])
                    ports.append(22)

                if 23 in work['ports']:
                    targets.append(work['ip'])
                    ports.append(23)


        if len(targets) == 0:
            print 'Brute monkey is waiting for something to brute force.  Eating bananas.  Will check again in 10 seconds.'
            time.sleep(10)

        else:
            print 'Brute monkey got work! Starting credential brute forcing!'

            index = randint(0,len(targets)-1)
            brutePort = ports[index]

            if brutePort == 21:
                ftpBrute(targets[index],db,hosts,monkeyId)

            elif brutePort == 22:
                sshBrute(targets[index],db,hosts,monkeyId)

            elif brutePort == 23:
                telBrute(targets[index],db,hosts,monkeyId)

def sshBrute(victim,db,coll,monkeyId):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(target, 22, usr, pwd)

    except paramiko.AuthenticationException:
        pass

    except socket.error:
        pass

def ftpBrute(victim,db,coll,monkeyId):
    print 'ftp bruting goes here.'


def telBrute (victim,db,coll,monkeyId):
    print 'telnet bruting goes here.'