#!/usr/bin/python
import os
import sys
import pymongo



def main():
    global options
    options = {}
    print "main"

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
        print "2-Define Monkeys"
        print "3-Unleash the Monkeys!"
        print "4-See the Monkey Business"
        print "5-Exit"
        print "\n"
        selection = raw_input("Select a menu option: ")
        
        if selection == "1":
            dbSetup()
        
        elif selection == "2":
            defMonkeys()
        
        elif selection == "3":
            startMonkeys()
        
        elif selection == "4":
            monkeyReport()
            
        elif selection == "5":
            sys.exit()
            
        else:
            raw_input("Press enter to continue.")
        

def dbSetup():
    print "\n\n"
    print "Database Setup:"
    print "---------------"
    msfDbIp = raw_input("Enter the IP address of the Metasploit Postgres instance: ")
    msfDbUser = raw_input("Enter the Metasploit Postgres username: ")
    msfDbPass = raw_input("Enter the Metasploit Postgres password: ")
    monkeyDbIp = raw_input("Enter the IP address of the Skiddiemonkey MongoDB instance: ")
    monkeyDbName = raw_input("Enter the name of the Skiddiemonkey Database: ")
    
    
        
        

if __name__ == '__main__':
	main()

