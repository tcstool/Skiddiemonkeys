#!/usr/bin/python

import socket
import sys
from thread import *
import scanmonkey
import pymongo
import fuzzymonkey


def main():
    startServer()
     
def startServer():
    print 'starting Skiddiemonkey server on port 7433'
    
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('',7433))
    
    except socket.error,e:
        print 'Failed to start listener.  Error code ' + str(e[0]) + 'Error message ' + str(e[1])
        sys.exit()
    
    s.listen(20)
    print 'Monkey is ready for work!'
    
def acceptWork(conn):
    conn.send('Monkey is listening.')
    
    while True:
        work = conn.recv(1024)
        reply = 'OK'
        
        if not work:
            break
        
        jobDetails = work.split(',')
        
        if jobDetails[0] == 'scan':
            scanmonkey.scanHosts()
        
        
        conn.sendall(reply)
        
    
    conn.close()


if __name__ == '__main__':
    main()