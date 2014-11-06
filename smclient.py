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
        conn = psycopg2.connect(database='msf3',host=msfDbIp,user=msfDbUser,password=msfDbPass)
        cur = con.cursor()
        cur.execute('SELECT file FROM module_details;')
        
        for sploit in cur:
            f = open(sploit[0],"r")
            portSearch = f.readlines()
            f.close()
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
    
    raw_input('targets loaded! presee enter to return to main menu.')
    return

def makeMonkeys():
   print 'making monkeys' 

if __name__ == '__main__':
    main()

