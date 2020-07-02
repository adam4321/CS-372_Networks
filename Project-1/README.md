# OSU CS-372 Project 1

A program which implements elements of a web client and server.
It is built in Python and uses the socket API. The program includes
3 different functions which are called from the command line. Functions
1 and 2 make different GET requests. The first is small and fits in a
single packet. The second is larger and needs to be parsed to allow the
client to receive the entire payload. The 3rd option is a simple server
which can be reached on localhost port 50000.

Example program calls:

GET request 1 =>    python project_1.py -c 1
GET request 2 =>    python project_1.py -c 2
Simple Server =>    python project_1.py -c 3