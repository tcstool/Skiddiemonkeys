#!/usr/bin/python

import paramiko
import ftplib
import socket
import time

def findLoginBoxes(runTime,dbIp,dbName,monkeyIq,monkeyLoc,monkeyId):
    timeout = time.time() + 60 * runTime

    while True:
        targets = []
        ports = []
        time.sleep(1)




def sshBute(targets,db,coll,monkeyId):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(target, 22, usr, pwd)

    except paramiko.AuthenticationException:
        pass

    except socket.error:
        pass


