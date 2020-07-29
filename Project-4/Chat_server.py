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
    s.bind((HOST, PORT))
    s.listen()
    
    # Display the host and port
    print(f'Server listening on: {HOST} on port: {PORT}')
    

    # Accept a client connection
    conn, addr = s.accept()

    conn_msg = "Type /q to quit\nEnter message to send..."
    conn.send(conn_msg.encode())
    

    # # If successful connection, then reply and then terminate
    # with conn:
    #     # Print out the connection information
    #     print()
    #     print("**************************************************")
    #     print(f"Connected by ({addr})")
    #     print("**************************************************")
    #     print("Waiting for message...\n")
        
    #     # Send the connection message to the client
    #     conn_msg = "Type /q to quit\nEnter message to send..."
    #     conn.send(conn_msg.encode())

    #     # Maintain a connection with the client until /q is received
    #     while True:
    #         data = conn.recv(2048)
    #         print(data.decode())

    #         # If the GET request is malformed, then exit the loop
    #         if not data:
    #             break

    #         # Test for /q connection close message
    #         if data.decode() == '/q':
    #             break


            # # Print server response to CLI
            # print("Server Sending")
            # print("**********************")
            # print(data)
            # print("**********************")

            # conn.sendall(data.encode())
            # break


    # Display the IP and PORT of the connected client
    print(f'Connected by ({addr[0]})')

    # Close the socket
    s.close()


if __name__ == '__main__':
    main()
