"""
Author:      Adam Wright
Email:       wrighada@oregonstate.edu
Date:        7/6/2020
Description: Adapted from companion material available for the textbook
             Computer Networking: A Top-Down Approach, 6th Edition
             Kurose & Ross ©2013. The program is a simple Python 3 
             implementation of the Linux program traceroute.
"""

from socket import *
import os
import sys
import struct
import time
import select
import binascii

ICMP_ECHO_REQUEST = 8
MAX_HOPS = 30
TIMEOUT  = 2.0
TRIES    = 2


# FUNCTION DEFINITIONS ------------------------------------------------------#

def checksum(string):
    csum = 0
    countTo = (len(string) // 2) * 2

    count = 0
    while count < countTo:
        thisVal = ord(string[count+1]) * 256 + ord(string[count])
        csum = csum + thisVal
        csum = csum & 0xffffffff
        count = count + 2

    if countTo < len(string):
        csum = csum + ord(string[len(string) - 1])
        csum = csum & 0xffffffff

    csum = (csum >> 16) + (csum & 0xffff)
    csum = csum + (csum >> 16)
    answer = ~csum
    answer = answer & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer


def build_packet(data_size):
    # Create a header with a zeroed checksum to pass to the checksum function
    # Struct contains 2 8 bit unsigned char fields and 1 16 bit unsigned short field
    header = struct.pack('!BBH', ICMP_ECHO_REQUEST, 0, 0)

    # The data passed in the packet are 2 unsigned short fields
    pid = os.getpid()
    data = struct.pack('!HH', pid, 1)
    valid_checksum = checksum(str(header + data))

    # Create the final header using the generated checksum
    header = struct.pack('!BBHHH', ICMP_ECHO_REQUEST, 0, valid_checksum, pid, 1)

    # Note: padding = bytes(data_size)
    padding = bytes(data_size)

    # Return the final packet
    packet = header + data + padding
    return packet

    
def get_route(hostname, data_size):
    timeLeft = TIMEOUT
    for ttl in range(1, MAX_HOPS):
        for tries in range(TRIES):

            destAddr = gethostbyname(hostname)

			# Make a raw socket named mySocket
            mySocket = socket(AF_INET, SOCK_RAW, IPPROTO_ICMP)
            
			# setsockopt method is used to set the time-to-live field.
            mySocket.setsockopt(IPPROTO_IP, IP_TTL, struct.pack('I', ttl))
            mySocket.settimeout(TIMEOUT)
            try:
                d = build_packet(data_size)
                mySocket.sendto(d, (hostname, 0))
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

            except timeout:
                continue

            else:
				# Fetch the icmp type from the IP packet
                # Remove the set of bytes representing the header
                icmp_header = recvPacket[20:28]
                types, code, checksum, pid, sequence = struct.unpack('!BBHHH', icmp_header)

                if types == 11:
                    bytes = struct.calcsize("d")
                    timeSent = struct.unpack("d", recvPacket[28:28 + bytes])[0]
                    print("  %d    rtt=%.0f ms    %s" %(ttl, (timeReceived -t)*1000, addr[0]))

                elif types == 3:
                    bytes = struct.calcsize("d")
                    timeSent = struct.unpack("d", recvPacket[28:28 + bytes])[0]
                    print("  %d    rtt=%.0f ms    %s" %(ttl, (timeReceived-t)*1000, addr[0]))

                elif types == 0:
                    bytes = struct.calcsize("d")
                    timeSent = struct.unpack("d", recvPacket[28:28 + bytes])[0]
                    print("  %d    rtt=%.0f ms    %s" %(ttl, (timeReceived - timeSent)*1000, addr[0]))
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

    # Print the arglist and Hostname
    print()
    print('Argument List: {0}'.format(str(sys.argv)))
    print(f'** Python Simple Traceroute to {trace_hostname}')
    print()

    # Run trace on the Hostname
    try:
        get_route(trace_hostname, data_size)
    except:
        print()
        print('Error: Traceroute ended')


if __name__ == '__main__':
    main()
