#!/bin/bash
#Skiddiemonkeys python dependency setup script


echo "This setup script will install pip and use it to load the necessary Python dependencies for Skiddiemonkeys on Red Hat and Debian based systems."
echo "It is EXPERIMENTAL and messes with your system.   Use at your own risk!!!"
echo "As far as installing Metasploit, you're on your own."
echo "Before we start, are you root? If not, this won't work."
echo -n "Continue (y/n)? "

read doIt

if  [ "$doIt" = "y" ] || [ "$doIt" = "Y" ]; then
	echo "You've been warned..."

	if [ -f /etc/debian_version ]; then
		echo "Debian-ish OS detected.  using apt-get to install pip."
		apt-get --force-yes install python-pip
		pip install pymongo
		pip install psycopg2
		pip install re
		pip install socket
		pip install time
		pip install random
		pip install sys
		pip install paramiko
		pip install ftplib
		pip install telnetlib
		pip install string
		pip install nmap
		pip install thread
		pip install subprocess
		pip install urllib2
		pip install ssl

		echo "All done.  Check output for errors. Have fun!"

	elif [ -f /etc/redhat-release ]; then
		echo "Red Hat-ish OS detected.  using yum to install pip."
		vernum=$(rpm -qa \*-release | grep -Ei "oracle|redhat|centos" | cut -d"-" -f3)

		if  [ "$vernum" = "6" ];then

			echo "version 6 detected.  Enabling repos."
			cd /tmp
			wget http://mirror-fpt-telecom.fpt.net/fedora/epel/6/i386/epel-release-6-8.noarch.rpm
			rpm -ivh epel-release-6-8.noarch.rpm
			yum -y install python-pip
		    pip install pymongo
		    pip install psycopg2
		    pip install re
		    pip install socket
		    pip install time
		    pip install random
		    pip install sys
		    pip install paramiko
		    pip install ftplib
		    pip install telnetlib
		    pip install string
		    pip install nmap
		    pip install thread
		    pip install subprocess
		    pip install urllib2
		    pip install ssl

			echo "All done.  Check output for errors. Have fun!"




		elif  [ "$vernum" = "5" ];then
			echo "version 5 detected.  Enabling repos."
			cd /tmp
			wget http://download.fedoraproject.org/pub/epel/5/i386/epel-release-5-4.noarch.rpm
			rpm -ivh epel-release-5-4.noarch.rpm
		    yum -y install python-pip
            pip install pymongo
		                pip install psycopg2
		                pip install re
		                pip install socket
		                pip install time
		                pip install random
		                pip install sys
		                pip install paramiko
		                pip install ftplib
		                pip install telnetlib
		                pip install string
		                pip install nmap
		                pip install thread
		                pip install subprocess
		                pip install urllib2
		                pip install ssl


			echo "All done.	 Check output for errors. Have fun!"

		fi

	fi
fi


exit 1
