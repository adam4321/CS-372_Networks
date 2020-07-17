"""
Author:      Adam Wright
Email:       wrighada@oregonstate.edu
Date:        7/6/2020
Description: Adapted from companion material available for the textbook
             Computer Networking: A Top-Down Approach, 6th Edition
             Kurose & Ross ©2013. The program is a simple Python 3 
             implementation of the Linux program traceroute.
"""

import socket
import os
import sys
import struct
import time
import select


# GLOBAL VARIABLES ----------------------------------------------------------#

ICMP_ECHO_REQUEST = 8
MAX_HOPS = 30
TIMEOUT  = 2
TRIES    = 2


# FUNCTION DEFINITIONS ------------------------------------------------------#

# Function to calculate the internet checksum
# The provided checksum function was not accepting the header format
# From the example implementation given by a TA
# https://github.com/James-P-D/Traceroute/blob/master/src/Tracert/Tracert/Tracert.py
# It follows rfc1071 https://tools.ietf.org/html/rfc1071
def calc_checksum(header):
    # Initialise checksum and overflow
    checksum = 0
    overflow = 0

    # For every word (16-bits)
    for i in range(0, len(header), 2):
        word = header[i] + (header[i+1] << 8)

        # Add the current word to the checksum
        checksum = checksum + word
        # Separate the overflow
        overflow = checksum >> 16
        # While there is an overflow
        while overflow > 0:        
            # Remove the overflow bits
            checksum = checksum & 0xFFFF
            # Add the overflow bits
            checksum = checksum + overflow
            # Calculate the overflow again
            overflow = checksum >> 16

    # There's always a chance that after calculating the checksum
    # across the header, there is *still* an overflow, so need to
    # check for that
    overflow = checksum >> 16
    while overflow > 0:        
        checksum = checksum & 0xFFFF
        checksum = checksum + overflow
        overflow = checksum >> 16

    # Ones-compliment and return
    checksum = ~checksum
    checksum = checksum & 0xFFFF

    return checksum


# Function to build the icmp packet which will be sent
def build_packet(data_size):
    # Get the process id of the Traceroute instance
    pid = os.getpid()
    cleared_checksum = 0

    # Create a header with a zeroed checksum to pass to the checksum function
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, cleared_checksum, pid, 1)
    valid_checksum = calc_checksum(header)

    # Create the final header using the generated checksum
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, valid_checksum, pid, 1)

    # Note: padding = bytes(data_size)
    data = bytes(data_size)

    # Return the final packet
    packet = header + data
    return packet


# Function to send the packet to the passed in hostname   
def get_route(hostname, data_size):
    timeLeft = TIMEOUT
    for ttl in range(1, MAX_HOPS):
        for tries in range(TRIES):

            # Make a raw socket named mySocket
            mySocket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
            
			# setsockopt method is used to set the time-to-live field.
            mySocket.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, struct.pack('I', ttl))
            mySocket.settimeout(TIMEOUT)
            
            try:
                d = build_packet(data_size)
                mySocket.sendto(d, (hostname, 1))

                t= time.time()
                startedSelect = time.time()
                whatReady = select.select([mySocket], [], [], timeLeft)
                howLongInSelect = (time.time() - startedSelect)

                if whatReady[0] == []: # Timeout
                    print("  *        *        *    Request timed out.")

                recvPacket, addr = mySocket.recvfrom(1024)
                timeReceived = time.time()
                timeLeft = timeLeft - howLongInSelect

                if timeLeft <= 0:
                    print("  *        *        *    Request timed out.")

            except socket.timeout:
                continue

            else:
				# Fetch the icmp type from the IP packet
                # Remove the set of bytes representing the header
                icmp_header = recvPacket[20:28]
                types, code, checksum, pid, sequence = struct.unpack('bbHHh', icmp_header)
                
                # Try to get the hostname of the destination
                dest_hostname = ''
                try:
                    destAddr = socket.gethostbyaddr(addr[0])
                    if len(destAddr[0]) > 0:
                        dest_hostname = destAddr[0]

                # If it fails then print nothing
                except:
                    dest_hostname = ''

                if types == 11:
                    print("  %d    rtt=%.0f ms    %s    %s" %(ttl, (timeReceived -t)*1000, addr[0], dest_hostname))

                elif types == 3:
                    print("  %d    rtt=%.0f ms    %s    %s" %(ttl, (timeReceived-t)*1000, addr[0], dest_hostname))

                elif types == 0:
                    print("  %d    rtt=%.0f ms    %s    %s" %(ttl, (timeReceived - t)*1000, addr[0], dest_hostname))
                    return

                else:
                    print("error")
                break

            finally:
                mySocket.close()


# MAIN ----------------------------------------------------------------------#

def main():
    data_size = 0

    # Make sure there are 1 or 2 CLI args and hostname is passed as CLI argument
    if len(sys.argv) == 1 or len(sys.argv) > 3:
        print("Error, Invalid call:  Traceroute.py [Hostname]")
        print("                   :  Traceroute.py [Hostname] [data_size]")
        return

    # Set the value of hostname
    elif len(sys.argv) == 2:
        trace_hostname = sys.argv[1]

    # Set the value of data_size if it is passed as a CLI option
    elif len(sys.argv) == 3:
        trace_hostname = sys.argv[1]
        data_size = int(sys.argv[2])

    # Try to get the hostname of the destination
    dest_hostname = ''
    try:
        destAddr = socket.gethostbyaddr(trace_hostname)
        if len(destAddr[0]) > 0:
            dest_hostname = '(' + str(destAddr[2][0]) + ')'

    # If it fails then print nothing
    except:
        dest_hostname = ''

    # Print the argument list, hostname, and destination IP if it is found
    print()
    print('Argument List: {0}'.format(str(sys.argv)))
    print(f'** Python Simple Traceroute {trace_hostname} {dest_hostname}')
    print()

    # Run trace on the Hostname
    try:
        get_route(trace_hostname, data_size)
    except:
        print()
        print('Error: Traceroute ended')


if __name__ == '__main__':
    main()
