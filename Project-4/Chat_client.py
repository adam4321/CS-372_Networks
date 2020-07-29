'''****************************************************************************
**  Author:       Adam Wright
**  Email:        wrighada@oregonstate.edu
**  Date:         7/27/2020
**  Description:  CS-372 Networks project 4. This project is to create a simple
**                chat server and client in Python. This file implements the
**                client side of the project. 
****************************************************************************'''

import socket

HOST = 'localhost'
PORT = 52000


# MAIN ---------------------------------------------------------------------- #

def main():
    try:
        # Create a TCP socket for the client
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))

        # Display a connection message
        print("\n***********************************************")
        print(f'Connected to: {HOST} on port: {PORT}')
    except:
        print("Error: No open server socket")
        return
    
    try:
        # Receive the server's initial message
        data = s.recv(2048)
        print(data.decode())

        # Client's initial message to the server
        data = input(">")

        # If the message is quit, then end the client connection
        if data[:2] == "/q":
            s.send(data.encode())
            s.close()
            return

        data += "\nType /q to quit\nEnter message to send..."
        s.send(data.encode())
    

        # Maintain a connection with the server until /q is received
        while True:
            # Recieve the server's message
            data = s.recv(2048)

            # Test for /q connection to close the connection
            if data.decode()[:2] == "/q":
                break
            else:
                print(data.decode())

            # Create and send the client's message
            data = input(">")
            s.send(data.encode())
        
            # If the message is quit, then end the client connection
            if data[:2] == "/q":
                break
                
    except:
        # Test for /q connection to close the connection
        if data[:2] == "/q":
            s.close()
            return
        else:
            print("Socket error")

    # Close the client socket
    s.close()


if __name__ == '__main__':
    main()
