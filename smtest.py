#!/usr/bin/python
#skiddemonkeys Copyright 2014 Russell Butturini
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

