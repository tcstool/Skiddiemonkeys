#!/usr/bin/python
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
    mmSelect = True
    
    while mmSelect:
        os.system('clear')
        print "     | |  (_)   | |   | (_)                            | |                 "
        print "  ___| | ___  __| | __| |_  ___   _ __ ___   ___  _ __ | | _____ _   _ ___ "
        print " / __| |/ / |/ _` |/ _` | |/ _ \ | '_ ` _ \ / _ \| '_ \| |/ / _ \ | | / __|"
        print ' \\__ \\   <| | (_| | (_| | |  __/ | | | | | | (_) | | | |   <  __/ |_| \\__ \\'
        print " |___/_|\_\_|\__,_|\__,_|_|\___| |_| |_| |_|\___/|_| |_|_|\_\___|\__, |___/"
        print "                                                                 __/  |     "
        print "                                                                 |___/      "
        print "Skiddiemonkeys v0.01-DEV"
        print "1-Set up the Database"
        print "2-Load targets"
        print "3-Define Monkeys"
        print "4-Unleash the Monkeys!"
        print "5-See the Monkey Business"
        print "6-Exit"
        print "\n"
        selection = raw_input("Select a menu option: ")
        
        if selection == "1":
            dbSetup()
        
        elif selection == "2":
            loadTargets()
        
        elif selection == "3":
            makeMonkeys()
        
        elif selection == "4":
            startMonkeys()
            
        elif selection == "5":
            monkeyReport()
            
        elif selection == "6":
            sys.exit()
            
        else:
            raw_input("Invalid selection.  Press enter to continue.")
        

def dbSetup():
    global options
    print "\n\n"
    print "Database Setup:"
    print "---------------"
    msfDbIp = raw_input("Enter the IP address of the Metasploit Postgres instance: ")
    msfDbUser = raw_input("Enter the Metasploit Postgres username: ")
    msfDbPass = raw_input("Enter the Metasploit Postgres password: ")
    monkeyDbIp = raw_input("Enter the IP address of the Skiddiemonkey MongoDB instance: ")
    monkeyDbName = raw_input("Enter the name of the Skiddiemonkey Database: ")
    options['dbip'] = monkeyDbIp
    options['dbname'] = monkeyDbName
    
    #We have to get the module names from the Metasploit DB for the monkeys and map the exploits to port numbers, so the sploit monkeys can
    #use the scanner monkey's work.
    
    try:
        pgConn = psycopg2.connect(database='msf3',host=msfDbIp,user=msfDbUser,password=msfDbPass)
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

    except:
        print "You wreck me baby."  #Placeholder for actually doing useful things

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

    try:
        db.monkeys.insert({'iq':monkeyIQ,'type':monkeyType,'location':monkeyLoc,'ip':monkeyIp})
        print 'Monkey Created!'

    except:
        print 'Failed to create monkey in database.'

   raw_input('Finished making monkeys.  Press enter to return to the main menu.')
   return

if __name__ == '__main__':
    main()

