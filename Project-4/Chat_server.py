'''****************************************************************************
**  Author:       Adam Wright
**  Email:        wrighada@oregonstate.edu
**  Date:         7/27/2020
**  Description:  CS-372 Networks project 4. This project is to create a simple
**                chat server and client in Python. This file implements the
**                server side of the project. 
****************************************************************************'''

import socket
import sys


HOST = 'localhost'
PORT = 52000

# FUNCTION DEFINITIONS ------------------------------------------------------ #

# Function to


# MAIN ---------------------------------------------------------------------- #

def main():
    # Create a TCP socket for the server 
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # Gather the 
    
    
    print(f'Server listening on: {HOST} on port: {PORT}')
    print(f'Connected by ()')
    s.close()


if __name__ == '__main__':
    main()
