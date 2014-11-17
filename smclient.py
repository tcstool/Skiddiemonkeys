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

import os
import sys
from pymongo import MongoClient
import psycopg2
import re


def main():
    global options
    options = {}
    mainMenu()

def mainMenu():
    mmValid = [1,2,3,4,5,6]
    selection = '99'
    while int(selection) not in mmValid:
        os.system('clear')
        print '     | |  (_)   | |   | (_)                            | |                 '
        print '  ___| | ___  __| | __| |_  ___   _ __ ___   ___  _ __ | | _____ _   _ ___ '
        print ' / __| |/ / |/ _` |/ _` | |/ _ \ | \'_ \` _ \ / _ \| \'_ \| |/ / _ \ | | / __|'
        print ' \\__ \\   <| | (_| | (_| | |  __/ | | | | | | (_) | | | |   <  __/ |_| \\__ \\'
        print ' |___/_|\_\_|\__,_|\__,_|_|\___| |_| |_| |_|\___/|_| |_|_|\_\___|\__, |___/'
        print '                                                                 __/  |     '
        print '                                                                 |___/      '
        print 'Skiddiemonkeys v0.01-DEV'
        print '1-Set up the Database'
        print '2-Load targets'
        print '3-Define Monkeys'
        print '4-Unleash the Monkeys!'
        print '5-See the Monkey Business'
        print '6-Exit'
        print '\n'
        selection = raw_input('Select a menu option: ')
        
        if selection == '1':
            selection = '99'
            dbSetup()
        
        elif selection == '2':
            selection = '99'
            loadTargets()
        
        elif selection == '3':
            selection = '99'
            makeMonkeys()
        
        elif selection == '4':
            selection = '99'
            startMonkeys()
            
        elif selection == '5':
            selection = '99'
            monkeyReport()
            
        elif selection == '6':
            sys.exit()
            
        else:
            raw_input('Invalid selection.  Press enter to continue.')
        

def dbSetup():
    global options
    print '\n\n'
    print 'Database Setup:'
    print '---------------'
    monkeyDbIp = raw_input('Enter the IP address of the Skiddiemonkeys MongoDB instance: ')
    monkeyDbName = raw_input('Enter the name of the Skiddiemonkey Database: ')
    options['dbip'] = monkeyDbIp
    options['dbname'] = monkeyDbName


    if raw_input('Do you want to import Metasploit modules for exploit monkeys to use? ').lower() == 'y':
        msfDbIp = raw_input('Enter the IP address of the Metasploit Postgres instance: ')
        msfDbUser = raw_input('Enter the Metasploit Postgres username: ')
        msfDbPass = raw_input('Enter the Metasploit Postgres password: ')
        msfDbName = raw_input('Enter the Metasploit Postgres DB name: ')

    #We have to get the module names from the Metasploit DB for the monkeys and map the exploits to port numbers, so the sploit monkeys can
    #use the scanner monkey's work.
    
        try:
            pgConn = psycopg2.connect(database=msfDbName,host=msfDbIp,user=msfDbUser,password=msfDbPass)
            cur = pgConn.cursor()
            cur.execute('SELECT file,fullname FROM module_details;')
            mongoConn = MongoClient(options['dbip'],27017)
            mongoDb = mongoConn[options['dbname']]

            if 'logins' in mongoDb.collection_names() or 'sploits' in mongoDb.collection_names():
                if raw_input('Previous exploit data found.  Erase? ').lower() == 'y':
                    if 'logins' in mongoDb.collection_names():
                        mongoDb['logins'].drop()

                    if 'sploits' in mongoDb.collection_names():
                        mongoDb['sploits'].drop()

            print 'Opening exploits and getting default port numbers...'
            for sploit in cur:
                f = open(sploit[0],"r")
                portSearch = f.readlines()
                f.close()
	    
                for line in portSearch:
                    if "Opt::RPORT" in line:
		    
                        try:
                            regex = '.*\((.*?)\).*'
                            matches = re.search(regex,line)

                            if matches.group(1).isdigit():
                                if 'auxiliary' in sploit[1] and 'scanner' in sploit[1] and  '_login' in sploit[1]:
                                    #If the logic evaluates to True, this is a login module
                                    mongoDb.logins.insert({'modName':sploit[1],'port':matches.group(1)})

                                elif 'exploit' in sploit[1]:
                                    #This is an exploit module
                                    mongoDb.sploits.insert({'modName':sploit[1],'port':matches.group(1)})

                            else:
                                continue

                        except:
                            pass

        except Exception,e:
            print 'Data not imported.  Check your MongoDB and Postgres settings. '  #Placeholder for actually doing useful things
            return

    raw_input('Database load complete! Press enter to return to the main menu.')
    return

def loadTargets():
    global options
    conn = MongoClient(options['dbip'],27017)
    db = conn[options['dbname']]
    
    if 'targets' in db.collection_names():
        if raw_input('Remove current list of targets? ').lower() == 'y':
            db['targets'].drop()

    else:
        print 'No targets found in database.'

    fileName = raw_input('Enter path to targets file: ')

    with open(fileName) as f:
        ipList = f.readlines()

    for target in ipList:
        db.targets.insert({'ip':target.split(',')[0],'value':target.split(',')[1],'location':target.split(',')[2].lower().rstrip()})
    
    raw_input('targets loaded! press enter to return to main menu.')
    return

def makeMonkeys():
   global options
   print 'Monkey setup'
   print '------------'
   conn = MongoClient(options['dbip'],27017)
   db = conn[options['dbname']]

   if 'monkeys' in db.collection_names():
        if raw_input('Existing monkeys found.  Remove?').lower() == 'y':
             db['monkeys'].drop()

   else:
      print 'No monkeys found in database.'
      
   numMonkeys = int(raw_input('Enter total numer of monkeys to create: '))
   validIQs = [0,1,2,3]
   validTypes = [1,2,3,4]
   validLocs = ['i','e']
   
   for i in range(1,numMonkeys+1):
    monkeyIQ = None
    monkeyType = None
    monkeyLoc = None
    print 'Setting up monkey #' + str(i)

    while monkeyIQ not in validIQs:
        print '---------------------'
        print 'Enter Monkey IQ:'
        print '0-World\'s #1 Hacker'
        print '1-CISSP'
        print '2-CEH'
        print '3-Security Weekly Listener'
        monkeyIQ = int(raw_input('Input: '))

    print "\n"
	
    while monkeyType not in validTypes:
        print 'Define Monkey Type:'
        print '1-Scanner Monkey'
        print '2-Exploit Monkey'
        print '3-Fuzzy Monkey'
        print '4-Login Monkey'
        print '5-Web Monkey'
        monkeyType = int(raw_input('Input: '))
	
    print "\n"
	
    while monkeyLoc not in validLocs:
        print 'Define Monkey Location:'
        print 'i-Internal'
        print 'e-External'
        monkeyLoc = raw_input('Input: ').lower()

    monkeyIp = raw_input('Enter IP address of monkey server: ')

    #Deal with fuzzy monkeys who need an extra option
    if monkeyType == 3:
        minFuzzSize = int(raw_input('Enter the minimum number of bytes of fuzz data to send: '))
        maxFuzzSize = int(raw_input('Enter the maximum number of bytes of fuzz data to send: '))

    try:
        if monkeyType == 3:
            db.monkeys.insert({'iq':monkeyIQ,'type':monkeyType,'location':monkeyLoc,'ip':monkeyIp,'min':minFuzzSize,'max':maxFuzzSize})

        else:
            db.monkeys.insert({'iq':monkeyIQ,'type':monkeyType,'location':monkeyLoc,'ip':monkeyIp})

        print 'Monkey Created!'

    except:
        print 'Failed to create monkey in database.'

   raw_input('Finished making monkeys.  Press enter to return to the main menu.')
   return

if __name__ == '__main__':
    main()

