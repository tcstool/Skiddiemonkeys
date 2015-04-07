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
-Nmap
-A default installation of MongoDB. Check [here](http://docs.mongodb.org/manual/installation/) for installation instructions.
-PyMongo python MongoDB drivers and libraries.
-Reachability from the client machines to TCP 7433 on the servers.
-Reachability to TCP 27017 on the MongoDB host from both the clients and the servers.

Other requirements vary based on the features in use:
- To use automated random exploit attempts, Metasploit with a functional Postgres backend is required.
- Various libraries required that a normal Python installation should have readily available. Your milage may vary, check the setup.sh script. 
 

Setup
============
``setup.sh``

Usage
=====
You will need at least 1 monkey server and 1 monkey client running (Both can technically be on the same machine but it's not a good idea).
To start the server:

``python smserver.py``
This starts a listener on TCP 7433 on the server for clients to connect to.  

To start the menu based CLI interface:
``python smclient.py``

To start the web interface using the Django built in web server:


NoSQLMap uses a menu based system for building attacks.  Upon starting NoSQLMap you are presented with with the main menu:

```
1-Set options (do this first)
2-NoSQL DB Access Attacks
3-NoSQL Web App attacks
4-Scan for Anonymous MongoDB Access
x-Exit
```


Explanation of options:
```
1. Set target host/IP-The target web server (i.e. www.google.com) or MongoDB server you want to attack.
2. Set web app port-TCP port for the web application if a web application is the target.
3. Set URI Path-The portion of the URI containing the page name and any parameters but NOT the host name (e.g. /app/acct.php?acctid=102).
4. Set HTTP Request Method (GET/POST)-Set the request method to a GET or POST; Presently only GET is implemented but working on implementing POST requests exported from Burp. 
5. Set my local Mongo/Shell IP-Set this option if attacking a MongoDB instance directly to the IP of a target Mongo installation to clone victim databases to or open Meterpreter shells to.
6. Set shell listener port-If opening Meterpreter shells, specify the port.
7. Load options file-Load a previously saved set of settings for 1-6.
8. Load options from saved Burp request-Parse a request saved from Burp Suite and populate the web application options.
9. Save options file-Save settings 1-6 for future use.
x. Back to main menu-Use this once the options are set to start your attacks.
```

Once options are set head back to the main menu and select DB access attacks or web app attacks as appropriate for whether you are attacking a NoSQL management port or web application. The rest of the tool is "wizard" based and fairly self explanatory, but send emails to nosqlmap@gmail.com or find me on Twitter [@tcstoolHax0r](https://twitter.com/tcstoolHax0r) if you have any questions or suggestions. 

Video
=====

NoSQLMap MongoDB Management Attack Demo.

<a href="http://www.youtube.com/watch?feature=player_embedded&v=xSFi-jxOBwM" target="_blank"><img src="http://img.youtube.com/vi/xSFi-jxOBwM/0.jpg" alt="NoSQLMap MongoDB Management Attack Demo" width="240" height="180" border="10" /></a> 

Contribute
==========

If you'd like to contribute, please create [new issue](https://github.com/tcstool/skiddiemonkeys/issues) or [pull request](https://github.com/tcstool/skiddiemonkeys/pulls).