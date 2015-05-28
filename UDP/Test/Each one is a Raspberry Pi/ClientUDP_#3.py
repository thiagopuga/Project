import socket
import sys
import time

NUMBER_MEASUREMENTS = 100

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ('169.254.0.1', 10000)

try:    
    for i in range(0, NUMBER_MEASUREMENTS):
        
        # Send data
        message = time.time()
        sent = sock.sendto(str(message).encode(), server_address)

finally:
    sock.close()
