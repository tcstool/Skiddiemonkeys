#!/usr/bin/python
#skiddiemonkeys Copyright 2014 Russell Butturini
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

import socket
import sys
from thread import *
import scanmonkey
import fuzzymonkey
import webmonkey
import brutemonkey
import sploitmonkey


def main():
    startServer()
     
def startServer():
    print 'starting Skiddiemonkey server on port 7433'
    
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('',7433))
    
    except socket.error,e:
        print 'Failed to start listener.  Error code ' + str(e[0]) + ' Error message ' + str(e[1])
        sys.exit()
    
    s.listen(20)
    print 'Monkey is ready for work!'

    while 1:
        conn, addr = s.accept()
        print 'Skiddiemonkey client at ' + addr[0] + ' connected.'
        start_new_thread(acceptWork,(conn,))

    
def acceptWork(conn):
    conn.send('Monkey is listening.')
    
    while True:
        work = conn.recv(1024)

        if not work:
            break
        
        jobDetails = work.split(',')

        if jobDetails[0] == '1':
            scanmonkey.scanHosts(int(jobDetails[3]),jobDetails[5],jobDetails[4],jobDetails[1],jobDetails[2],int(jobDetails[6]))

        if jobDetails[0] == '2':
            sploitmonkey.findTargets(int(jobDetails[3]),jobDetails[5],jobDetails[4],jobDetails[1],jobDetails[2],int(jobDetails[6]))

        elif jobDetails[0] == '3':
            fuzzymonkey.fuzzPorts(int(jobDetails[3]),jobDetails[5],jobDetails[4],jobDetails[1],jobDetails[2],jobDetails[6],jobDetails[7],int(jobDetails[8]))

        elif jobDetails[0] == '4':
            brutemonkey.findLoginBoxes(int(jobDetails[3]),jobDetails[5],jobDetails[4],jobDetails[1],jobDetails[2],int(jobDetails[6]))

        elif jobDetails[0] == '5':
            webmonkey.findWebBoxes(int(jobDetails[3]),jobDetails[5],jobDetails[4],jobDetails[1],jobDetails[2],int(jobDetails[6]))
    
    conn.close()


if __name__ == '__main__':
    main()