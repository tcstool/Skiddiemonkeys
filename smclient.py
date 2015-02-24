#!/usr/bin/python
# skiddiemonkeys Copyright 2014 Russell Butturini
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
import socket
import time
from random import randint


def main():
    global options
    global monkeyIds
    options = {}
    monkeyIds = []
    options['CLI'] = 'true'
    mainMenu()


def mainMenu():
    mmValid = [1, 2, 3, 4, 5, 6]
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
            selection = '99'
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
        dbLoadModules(options, msfDbIp, msfDbUser, msfDbPass, msfDbName)
    raw_input('Database load complete! Press enter to return to the main menu.')
    return
    #We have to get the module names from the Metasploit DB for the monkeys and map the exploits to port numbers, so the sploit monkeys can
    #use the scanner monkey's work.


def dbLoadModules(options, msfDbIp, msfDbUser, msfDbPass, msfDbName):
    try:
        pgConn = psycopg2.connect(database=msfDbName, host=msfDbIp, user=msfDbUser, password=msfDbPass)
        cur = pgConn.cursor()
        cur.execute('SELECT file,fullname FROM module_details;')
        mongoConn = MongoClient(options['dbip'], 27017)
        mongoDb = mongoConn[options['dbname']]

        if 'logins' in mongoDb.collection_names() or 'sploits' in mongoDb.collection_names():
            if (options['CLI'] == 'true' and raw_input('Previous exploit data found.  Erase? ').lower() == 'y') or (
                            options['CLI'] == 'false' and options['eraseSploitData'] == 'true'):
                if 'logins' in mongoDb.collection_names():
                    mongoDb['logins'].drop()

                if 'sploits' in mongoDb.collection_names():
                    mongoDb['sploits'].drop()

        print 'Opening exploits and getting default port numbers...'
        for sploit in cur:
            f = open(sploit[0], "r")
            portSearch = f.readlines()
            f.close()

            for line in portSearch:
                if "Opt::RPORT" in line:

                    try:
                        regex = '.*\((.*?)\).*'
                        matches = re.search(regex, line)

                        if matches.group(1).isdigit():
                            if 'auxiliary' in sploit[1] and 'scanner' in sploit[1] and '_login' in sploit[1]:
                                #If the logic evaluates to True, this is a login module
                                mongoDb.logins.insert({'modName': sploit[1], 'port': matches.group(1)})

                            elif 'exploit' in sploit[1]:
                                #This is an exploit module
                                mongoDb.sploits.insert({'modName': sploit[1], 'port': matches.group(1)})

                        else:
                            continue

                    except:
                        pass

    except Exception, e:
        if options['CLI'] == 'true':
            raw_input('Data not imported.  Check your MongoDB and Postgres settings. ')
        return


def loadTargets():
    global options
    conn = MongoClient(options['dbip'], 27017)
    db = conn[options['dbname']]

    if 'targets' in db.collection_names():
        if raw_input('Remove current list of targets? ').lower() == 'y':
            db['targets'].drop()

    else:
        print 'No targets found in database.'

    fileName = raw_input('Enter path to targets file: ')

    loadTargetsParam(options, fileName, db)
    raw_input('targets loaded! press enter to return to main menu.')
    return


def loadTargetsParam(options, fileName, db):
    if options['CLI'] == 'false' and options['eraseTargetsData'] == 'true':
        db['targets'].drop()

    with open(fileName) as f:
        ipList = f.readlines()

    for target in ipList:
        db.targets.insert({'ip': target.split(',')[0], 'value': target.split(',')[1],
                           'location': target.split(',')[2].lower().rstrip()})


def makeMonkeys():
    global options
    global monkeyIds
    monkeyTypes = [None,'Scan Monkey',None,'Fuzzy Monkey',None,'Web Monkey']
    dropSel = True
    existing = []
    print 'Monkey setup'
    print '------------'
    conn = MongoClient(options['dbip'], 27017)
    db = conn[options['dbname']]

    if 'monkeys' in db.collection_names():
        if raw_input('Existing monkeys found.  Remove? ').lower() == 'y':
            count = 1

            for monkey in db.monkeys.find():
                print str(count) + '-' + str(monkey['ip']) + '-' + monkeyTypes[ int(monkey['type']) ]
                existing.append(monkey['id'])
                count += 1

            while dropSel == True:
                dropSel = raw_input('Enter monkey to remove,e to remove all monkeys, or q to make monkeys: ')

                if  dropSel.lower() == 'e':
                    db['monkeys'].drop()
                    print 'Monkeys removed!'

                elif dropSel.lower() == 'q':
                    dropSel = False

                else:
                    db.monkeys.remove({'id' : existing[int(dropSel)-1]})
                    dropSel = True


        else:
            #Get the IDs of the existing monkeys to avoid dupes
            for monkey in db.monkeys.find():
                monkeyIds.append(monkey['id'])

    else:
        print 'No monkeys found in database.'

    numMonkeys = int(raw_input('Enter total number of monkeys to create: '))
    validIQs = [0, 1, 2, 3]
    validTypes = [1, 2, 3, 4, 5]
    validLocs = ['i', 'e']

    monkeyIQ = {}
    monkeyType = {}
    monkeyLoc = {}
    monkeyIp = {}
    minFuzzSize = {}
    maxFuzzSize = {}
    for i in range(1, numMonkeys + 1):
        monkeyIQ[i] = None
        monkeyType[i] = None
        monkeyLoc[i] = None
        print 'Setting up monkey #' + str(i)

        while monkeyIQ[i] not in validIQs:
            print '---------------------'
            print 'Enter Monkey IQ:'
            print '0-World\'s #1 Hacker'
            print '1-CISSP'
            print '2-CEH'
            print '3-Security Weekly Listener'
            monkeyIQ[i] = int(raw_input('Input: '))

        print "\n"

        while monkeyType[i] not in validTypes:
            print 'Define Monkey Type:'
            print '1-Scanner Monkey'
            print '2-Exploit Monkey'
            print '3-Fuzzy Monkey'
            print '4-Brute Monkey'
            print '5-Web Monkey'
            monkeyType[i] = int(raw_input('Input: '))

        print "\n"

        while monkeyLoc[i] not in validLocs:
            print 'Define Monkey Location:'
            print 'i-Internal'
            print 'e-External'
            monkeyLoc[i] = raw_input('Input: ').lower()

        monkeyIp[i] = raw_input('Enter IP address of monkey server: ')

        #Deal with fuzzy monkeys who need an extra option
        if monkeyType[i] == 3:
            minFuzzSize[i] = int(raw_input('Enter the minimum number of bytes of fuzz data to send: '))
            maxFuzzSize[i] = int(raw_input('Enter the maximum number of bytes of fuzz data to send: '))

    loadMonkeys(options, db, monkeyIQ, monkeyType, monkeyLoc, monkeyIp, minFuzzSize, maxFuzzSize)
    raw_input('Finished making monkeys.  Press enter to return to the main menu.')
    return


def loadMonkeys(options, db, monkeyIQ, monkeyType, monkeyLoc, monkeyIp, minFuzzSize, maxFuzzSize):
    randId = None
    global monkeyIds
    #Get in that barrel!
    if options['CLI'] == 'false' and options['eraseMonkeyData'] == 'true':
        db['monkeys'].drop()
    count = 1

    for i in monkeyIQ:
        try:
            #generate random monkey identifier
            while randId not in monkeyIds:
                randId = randint(1,1000000)
                monkeyIds.append(randId)


            if monkeyType[i] == 3:
                db.monkeys.insert(
                    {'id': randId, 'iq': monkeyIQ[i], 'type': monkeyType[i], 'location': monkeyLoc[i], 'ip': monkeyIp[i],
                     'min': minFuzzSize[i], 'max': maxFuzzSize[i]})
                randId = None

            else:
                db.monkeys.insert({'id': randId, 'iq': monkeyIQ[i], 'type': monkeyType[i], 'location': monkeyLoc[i],
                                   'ip': monkeyIp[i]})
                randId = None

            print 'Monkey', count, 'Created!'
            count += 1

        except:
            print 'Failed to create monkey in database.'


def startMonkeys():
    global options
    conn = MongoClient(options['dbip'], 27017)
    db = conn[options['dbname']]

    if 'actions' in db.collection_names() or 'hosts' in db.collection_names():
        if raw_input('Previous monkey attacks found.  Erase? ').lower() == 'y':
            db['actions'].drop()
            db['hosts'].drop()


    options['runTime'] = raw_input('How many minutes should the monkeys be loose? ')
    startMonkeysParam(options, db)

    print 'Fly my pretties, fly!'
    timeout = time.time() + 60 * int(options['runTime'])

    while True:
        if time.time() > timeout:
            raw_input('End of the day! Punching out. Check servers to make sure all work is done.\nPress enter to return to the main menu.')
            break

def startMonkeysParam(options, db):
    for monkey in db.monkeys.find():
        #Get each monkey from the database and transmit instructions to the server

        if monkey['type'] == 3:  #Fuzzy monkeys require extra instructions
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((monkey['ip'], 7433))
                work = str(monkey['type']) + ',' + str(monkey['iq']) + ',' + monkey['location'] + ',' + options[
                    'runTime'] + ',' + options['dbname'] + ',' + options['dbip'] + ',' + str(monkey['min']) + ',' + str(
                    monkey['max']) +',' + str(monkey['id'])
                s.send(work)
                s.close()

            except Exception, e:
                print e  #debug
                print 'Error: Couldn\'t connect to monkey at ' + monkey['ip']
                continue

        else:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((monkey['ip'], 7433))
                work = str(monkey['type']) + ',' + str(monkey['iq']) + ',' + monkey['location'] + ',' + options[
                    'runTime'] + ',' + options['dbname'] + ',' + options['dbip'] + ',' + str(monkey['id'])
                s.send(work)
                s.close()

            except Exception, e:
                print e  #debug
                print 'Error: Couldn\'t connect to monkey at ' + monkey['ip']
                continue


def monkeyReport():
    global options
    conn = MongoClient(options['dbip'],27017)
    db = conn[options['dbname']]

    print 'Monkeys clocking out'
    print '===================='

    validTypes = [1, 2]
    print 'Select format for output:'
    print '1-CSV'
    print '2-HTML'
    outType = int(raw_input('Input: '))

    if outType not in validTypes:
        raw_input('Invalid output selection.  Press enter to return.')

    else:
        savePath = raw_input('Enter file name to save: ')


        fo = open(savePath, 'wb')

        if outType == 1:  #Write CSV header row
            fo.write('action,attacker,target,starttime,endtime,fuzzport,fuzzbytes,\n')

        for event in db.actions.find(): # loop through events
            if outType == 1:
                if event['action'] == 'fuzz':
                    fo.write(event['action']+','+ str(db.monkeys.find_one({'id' : event['id']})['ip']) +','+event['ip']+','+event['start']+','+event['end']+ ',' + event['port'] + ',' + event['bytes'] +'\n')

                else:
                    fo.write(event['action']+','+ str(db.monkeys.find_one({'id' : event['id']})['ip']) +','+event['ip']+','+event['start']+','+event['end']+',NA,NA\n')

        raw_input('\nAll done! Press enter to return to the main menu.')
        return


if __name__ == '__main__':
    main()

