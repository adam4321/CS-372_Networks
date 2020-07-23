# Project-2 Simple Traceroute - OSU CS-372 

The program is a simple Python 3 implementation of the Linux program traceroute.

The program must be called with sudo, because only the Root user can open raw 
sockets. The program is built for Python3. There is an optional final argument 
to pass in the size of the data payload, which is currently set to be filled
with zeros.

Example program call:  $ sudo python3 Traceroute.py hostname.tld
Optional argument      $ sudo python3 Traceroute.py hostname.tld 64