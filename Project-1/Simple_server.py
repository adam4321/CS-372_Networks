"""
Author:         Adam Wright
Email:          wrighada@oregonstate.edu
Date:           6/27/2020 
Description:    Project 1 from OSU CS-372 Summer 2020. The project uses the
                Python socket API to make a GET request and then uses it to
                create a very simple web server.
"""

import socket

# Global targets for the Client requests 
TARGET_PORT = 80
TARGET_URL = "gaia.cs.umass.edu"
TARGET_HOST = "HTTP/1.1\r\nHost:gaia.cs.umass.edu\r\n\r\n"


# Create a new socket instance and connect to required URL
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TARGET_URL, TARGET_PORT))


# Form and make the 1st GET request
request ="GET /wireshark-labs/INTRO-wireshark-file1.html " + TARGET_HOST
s.send(request.encode())

# Print out the connection information and get request response text
print("**********************\n")
print(f"Request:{request}")

# Recieve the reply and print to console
response = s.recv(2048)  
print(response.decode())

# Form and make the 2nd GET request
request_2 = "GET /wireshark-labs/HTTP-wireshark-file3.html " + TARGET_HOST
s.send(request.encode())

# Close the socket
s.close()
