"""
Author:      Adam Wright
Email:       wrighada@oregonstate.edu
Date:        7/6/2020
Description: Adapted from companion material available for the textbook
             Computer Networking: A Top-Down Approach, 6th Edition
             Kurose & Ross ©2013
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
    # First, make the header of the packet, then append the checksum to the header,
    # then finally append the data

    # Create a header with a zeroed checksum to pass to the checksum function
    # Struct contains 2 8 bit unsigned char fields and 3 16 bit unsigned short fields
    pid = os.getpid()
    header = struct.pack('!BBHHH', ICMP_ECHO_REQUEST, 0, 0, pid, 1)

    # The data passed in the packet
    data = bytes(52)
    valid_checksum = checksum(str(header + data))

    # Create the final header using the generated checksum
    header = struct.pack('!BBHHH', ICMP_ECHO_REQUEST, 0, valid_checksum, pid, 1)

    # Note: padding = bytes(data_size)
    padding = bytes(data_size)

    # Don’t send the packet yet, just return the final packet in this function.
    # So the function ending should look like this
    packet = header + data + padding
    return packet

    
def get_route(hostname,data_size):
    timeLeft = TIMEOUT
    for ttl in range(1,MAX_HOPS):
        for tries in range(TRIES):

            destAddr = gethostbyname(hostname)

			# SOCK_RAW is a powerful socket type. 
            # For more details:   http://sock-raw.org/papers/sock_raw
			# Fill in start
			# Make a raw socket named mySocket
            mySocket = socket(AF_INET, SOCK_RAW, IPPROTO_ICMP)

			# Fill in end
            
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
				# Fill in start
				# Fetch the icmp type from the IP packet
                # Remove the set of bytes representing the header
                icmp_header = recvPacket[20:28]
                types, code, checksum, pid, sequence = struct.unpack('!BBHHH', icmp_header)
				# Fill in end

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
    if len(sys.argv) == 2:
        trace_hostname = sys.argv[1]

    if len(sys.argv) >= 3:
        data_size = int(sys.argv[2])

    print()
    print('Argument List: {0}'.format(str(sys.argv)))
    print(f'** Python Simple Traceroute to {trace_hostname}')
    print()

    try:
        get_route(trace_hostname, data_size)
    except:
        print('Error: Traceroute ended')


if __name__ == '__main__':
    main()
