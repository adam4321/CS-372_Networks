'''****************************************************************************
**  Author:       Adam Wright
**  Email:        wrighada@oregonstate.edu
**  Date:         7/27/2020
**  Description:  CS-372 Networks project 4. This project is to create a simple
**                chat server and client in Python. This file implements the
**                server side of the project. 
****************************************************************************'''

import socket

HOST = 'localhost'
PORT = 52000


# MAIN ---------------------------------------------------------------------- #

def main():
    # Create a TCP socket for the server 
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(5)
    
    # Display the host and port
    print()
    print(f'Server listening on: {HOST} on port: {PORT}')
    
    # Accept a client connection
    conn, addr = s.accept()

    # If connection was successful
    if conn:
        # Print connection information to the CLI
        print("**************************************************")
        print(f"Connected by {addr}")
        print("Waiting for message...")
        
        # Send the connection message to the client
        connect_msg = "Type /q to quit\nEnter message to send..."
        conn.send(connect_msg.encode())
        
        # Recieve the clients message
        data = conn.recv(2048)

        # Test for /q connection to close the connection
        if data.decode()[:2] == "/q":
            s.close()
            return
        else:
            print(data.decode())

        
        # Maintain a connection with the client until /q is received
        while True:
            # Create server message and send to client
            data = input(">")
            conn.send(data.encode())

            # If the message is quit, then close the connection
            if data[:2] == "/q":
                break

            # Recieve the clients message and print
            data = conn.recv(2048)

            # Test for /q connection to close the connection
            if data.decode()[:2] == "/q":
                break
            else:
                print(data.decode())
        

    # Print an error if the connection failed
    else:
        # Test for /q connection to close the connection
        if data[:2] == "/q":
            s.close()
            return
        else:
            print("Socket error")

    # Close the socket
    s.close()
                

if __name__ == '__main__':
    main()
