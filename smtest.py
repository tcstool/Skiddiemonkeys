#!/usr/bin/python

import scanmonkey
import fuzzymonkey

def main():
    print 'SkiddieMonkey PoC Front End Tester'
    fileName = raw_input('ip list file name: ')
    runtime = int(raw_input('minutes to run: '))
    dbName = raw_input('Target MongoDB name: ')
    
    with open (fileName) as f:
        ipList = f.readlines()
    
    #scanmonkey.scanHosts(ipList,int(runtime),dbName)
    fuzzymonkey.fuzzPorts(int(runtime),dbName)
   


if __name__ == '__main__':
	main()

