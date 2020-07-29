'''****************************************************************************
**  Author:       Adam Wright
**  Email:        wrighada@oregonstate.edu
**  Date:         7/27/2020
**  Description:  CS-372 Networks project 4. This project is to create a simple
**                chat server and client in Python. This file implements the
**                client side of the project. 
****************************************************************************'''

import socket
import sys

HOST = 'localhost'
PORT = 52000

# FUNCTION DEFINITIONS ------------------------------------------------------ #

# Function to


# MAIN ---------------------------------------------------------------------- #

def main():
    # Create a TCP socket for the client
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

    # Display a connection message
    print(f'Connected to: {HOST} on port: {PORT}')
    response = s.recv(2048)
    print(response.decode())

    # while True:
    #     message = s.recv(2048) 
    #     print(message)

    close_msg = "/q"
    s.send(close_msg.encode())

    # Close the client socket
    s.close()


if __name__ == '__main__':
    main()
