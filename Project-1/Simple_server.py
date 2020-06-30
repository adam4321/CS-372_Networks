"""
Author:         Adam Wright
Email:          wrighada@oregonstate.edu
Date:           6/27/2020 
Description:    Project 1 from OSU CS-372 Summer 2020. The project uses the
                Python socket API to make a GET request and then uses it to
                create a very simple web server.
"""

import socket
import sys
import re


## Global variables  ##########################################################

# Global targets for the Client requests 
TARGET_PORT = 80
TARGET_URL = "gaia.cs.umass.edu"
TARGET_HOST = "HTTP/1.1\r\nHost:gaia.cs.umass.edu\r\n\r\n"

# Global targts for the simple server
HOST = "127.0.0.1"
PORT = 50000


## FUNCTION DEFINITIONS  ######################################################

# Python replacement for switch statement - chooses function pointer
def switcher(arg):
    switcher = {
        "1": first_GET,
        "2": second_GET,
        "3": simple_server
    }

    # Return the correct function definition or the string nothing
    return switcher.get(str(arg), "incorrect argument")


# First GET request
def first_GET(s):
    # 1st request
    request ="GET /wireshark-labs/INTRO-wireshark-file1.html " + TARGET_HOST

    # Connect to required URL and make the 1st GET request
    s.connect((TARGET_URL, TARGET_PORT))
    s.send(request.encode())

    # Print out the connection information and get request response text
    print()
    print("**********************")
    print("GET request 1")
    print("**********************")
    print(f"Request:{request}")

    # Recieve the reply and print to console
    response = s.recv(2048)  
    print(response.decode())
    print("**********************")


def second_GET(s):
    # Second request
    request_2 = "GET /wireshark-labs/HTTP-wireshark-file3.html " + TARGET_HOST

    # Connect to required URL and make the 2nd GET request
    s.connect((TARGET_URL, TARGET_PORT))
    s.send(request_2.encode())

    # Print out the connection information and get request response text
    print()
    print("**********************")
    print("GET request 2")
    print("**********************")
    print(f"Request:{request_2}")

    pattern = re.compile("</html>")

    # Recieve the reply and print to console
    while True:
        response = s.recv(2048)
        if not pattern.search(str(response)):
            print(response.decode())
        elif len(response) <= 0:
            break
        else:
            print(response.decode())
            break

    print()
    print("**********************")


def simple_server(s):
    print("Hello!")


## MAIN #######################################################################

def main():
    # Create a new socket instance
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Call the switch statement with the passed in argument
    if len(sys.argv) == 3:
        called_func = switcher(sys.argv[2])
        if called_func != "incorrect argument":
            called_func(s)
        else:
            print("\nError: You must enter -c [1 or 2] as CLI argument")
    else:
        print("\nError: You must enter -c [1 or 2] as CLI argument")
        
    # Close the socket
    s.close()


# Declare the file's entry point
if __name__ == "__main__":
    main()
