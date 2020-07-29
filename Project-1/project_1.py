"""
Author:         Adam Wright
Email:          wrighada@oregonstate.edu
Date:           6/27/2020 
Description:    Project 1 from OSU CS-372 Summer 2020. The project uses the
                Python socket API to make a 2 GET requests and then uses it to
                create a very simple web server which can be reached from a local
                web browser on 127.0.0.1 port 50000.
"""

import socket
import sys
import re
from time import sleep


## Global variables  ##########################################################

# Global targets for the Client requests 
TARGET_PORT = 80
TARGET_URL = "gaia.cs.umass.edu"
TARGET_HOST = "HTTP/1.1\r\nHost:gaia.cs.umass.edu\r\n\r\n"

# Global targts for the Simple Server
HOST = "localhost"
PORT = 50500


## FUNCTION DEFINITIONS  ######################################################

# Python replacement for switch statement - chooses function pointer
def switcher(arg):
    switcher = {
        "1": first_GET,
        "2": second_GET,
        "3": simple_server
    }

    # Return the correct function definition or the string "incorrect argument"
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
    # 2nd request
    request = "GET /wireshark-labs/HTTP-wireshark-file3.html " + TARGET_HOST

    # Connect to required URL and make the 2nd GET request
    s.connect((TARGET_URL, TARGET_PORT))
    s.send(request.encode())

    # Print out the connection information and get request response text
    print()
    print("**********************")
    print("GET request 2")
    print("**********************")
    print(f"Request:{request}")

    # Pattern at the end of the transmission
    pattern = re.compile("</html>")

    # Recieve the reply and print to console
    while True:
        response = s.recv(2048)

        # Use regex to find the ending </html> in the transmission
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
    # Reuse existing socket and Bind socket to Localhost and listen for 30 sec.
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.settimeout(30)
    s.bind((HOST, PORT))
    s.listen()

    print("\nConnect to 127.0.0.1:50000 from your web browser")
    print("Simple Server started...\n")

    try:
        # Accecpt an incoming connection
        conn, addr = s.accept()

        # If successful connection, then reply and then terminate
        with conn:
            # Print out the connection information and get request response text
            print()
            print("**********************")
            print("Server Received")
            print("**********************")
            print('Connected by', addr, "\n")


            # Maintain loop until connection fails or succeeds and response is sent
            while True:
                data = conn.recv(2048)
                print(data.decode())
                print("**********************")

                # If the GET request is malformed, then exit the loop
                if not data:
                    break

                # Server response payload
                data = "HTTP/1.1 200 OK\r\n"\
                        "Content-Type: text/html; charset=UTF-8\r\n\r\n"\
                        "<html>Congratulations! You've downloaded the"\
                        " first Wireshark lab file!</html>\r\n"

                # Print server response to CLI
                print("Server Sending")
                print("**********************")
                print(data)
                print("**********************")

                conn.sendall(data.encode())
                break
    except:
        print("\nTimeout Error: Connection must be made within 30 seconds")
        

## MAIN #######################################################################

def main():
    error_msg = "\nError: You must enter -c [1 or 2 or 3] as CLI argument\n"\
                "If option 3, then you must visit 127.0.0.1:5000 within your browser"

    # CLI arg count must be 3
    if len(sys.argv) == 3:
        called_func = switcher(sys.argv[2])

        # Call the switch statement with the passed in CLI argument
        if called_func != "incorrect argument":
            # Create a new socket instance
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Call the requested function
            called_func(s)

            # Close the socket
            s.close()
        else:
            print(error_msg)
    else:
        print(error_msg)
        

# Declare the file's entry point
if __name__ == "__main__":
    main()
