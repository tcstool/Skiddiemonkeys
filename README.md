Skiddiemonkeys 
========

[Skiddiemonkeys](http://www.skiddiemonkeys.net) v0.1

Introduction
============
The goal of the Skiddiemonkeys project is to create an open source, simple to deploy system for blue teams to safely simulate malicious activity in a distributed fashion to identify gaps and weaknesses in detective and preventative controls.  It is written in Python 2.7 and has both a menu based CLI interface, as well as a web front end.  
The system operates as a client-server model, with a centralized application distributing "work" (i.e. bad actions) to listening servers to perform.

Requirements 
============
On a Debian or Red Hat based system, the setup.sh script may be run as root to automate the installation of several of the Skiddiemonkey dependencies.  

Required:
- Nmap
- A default installation of MongoDB. Check [here](http://docs.mongodb.org/manual/installation/) for installation instructions.
- PyMongo python MongoDB drivers and libraries.
- Reachability from the client machines to TCP 7433 on the servers.
- Reachability to TCP 27017 on the MongoDB host from both the clients and the servers.

Other requirements vary based on the features in use:
- To use automated random exploit attempts and payloads, Metasploit with a functional Postgres backend is required.
- Various libraries required that a normal Python installation should have readily available for installation with pip or easyinstall. Your milage may vary, check the setup.sh script. 

Setup
============
``setup.sh`` This is a helper script to manage installing some of the Python dependencies.

Usage
=====
You will need at least 1 monkey server and 1 monkey client running (Both can technically be on the same machine but it's not a good idea).
To start the server:

``python smserver.py``
This starts a listener on TCP 7433 on the server for clients to connect to.  

To start the menu based CLI interface:
``python smclient.py``

To start the web interface using the Django built in web server:
``python manage.py runserver``

The web interface generally follows the same flow as the CLI interface, which uses a menu based system for building the simulation.  Upon starting Skiddiemonkeys you are presented with with the main menu.  The meny is structured such that the options are presented in the order they need to be used for the application flow.

```
Skiddiemonkeys v0.1
1-Set up the Database
2-Load targets
3-Define Monkeys
4-Unleash the Monkeys!
5-See the Monkey Business
6-Exit
```


Explanation of menu items:
<h3>Set up the database</h3>
Set options to specify the IP of the MongoDB server and database parameters.  NOTE:  DO NOT USE 127.0.0.1 HERE.  This is the IP that will be transmitted to the servers to connect to as well.  
If using Metasploit, this will also allow specification of options to load the Metasploit exploit port mappings into MongoDB.
<b>The default installation of Postgres with Metasploit only binds to the loopback address.  You will need to use 127.0.0.1 if you have not configured postgres to allow remote connections.</b>

<h3>Load Targets</h3>
A comma separated target list in a text file will need to be provided.  The format is as follows:
``IP,value,location``
- IP-The IP address the monkeys should attack.

- Value-a numeric value from 0 to 3 which defines the criticality of the target and the data it holds.

- Location-specify i for internal or e for external.  Monkeys with a matching defined location are eligible to attack this target.
 
<h3>Define Monkeys</h3>
First, Skiddiemonkeys will ask how many monkeys to create.  For each created monkey, the following will need to be specified:
- Monkey IQ Ranging from 0 to 3.  The lower the monkey IQ, the more likely it is to waste time on low value targets, or targets already attacked.
- Monkey Type.  There are various types of bad actors (aka "monkeys") which can be defined:<br>
<i>Scan Monkey-</i>These monkeys are port scanners which will scan random targets in the provided CSV file.  One scan monkey is always required on a blank database to provide network facing service data to the other monkeys for them to attack.<br>
<i>Exploit Monkey-</i>These monkeys will launch random Metasploit exploits with random payloads based on open ports on a random target.<br>
<i>Fuzzy Monkey-</i>These monkeys will send random amounts of data within a specified range at random ports on a target.<br>
<i>Brute Monkey-</i>These monkeys will launch dictionary password attacks using common default credentials against SSH and FTP servers.<br>
<i>Web Monkey-</i>These monkeys will perform directory brute forcing against exposed web servers using common directory names.<br>

Lists that the web and brute monkeys use are in the lists subfolder in the Github repository (weblist.txt for the web monkey, wordlist_ftp.txt and wordlist_ssh.txt for the brute force monkey).  These can be replaced with another list as long as they follow the username:password format for the brute forcer, and just a straight wordlist for web directories.


- Monkey Location
Specify the location of the monkey server.  This defines eligibility to attack targets based on the value associated with the target in the CSV file.

<h3>Unleash the Monkeys!</h3>
Specify the number of minutes for the monkeys to attack the targets provided.  This information will be transmitted to the monkey servers along with the other defined attributes and the events will begin.

<h3>See the Monkey Business</h3>
Generate a report of all the bad actions generated by the monkeys during the run.  Currently only CSV output is supported.


 [@tcstoolHax0r](https://twitter.com/tcstoolHax0r) if you have any questions or suggestions. 

Contribute
==========

If you'd like to contribute, please create [new issue](https://github.com/tcstool/skiddiemonkeys/issues) or [pull request](https://github.com/tcstool/skiddiemonkeys/pulls).