import socket
import sys
import time

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ("169.254.0.1", 10000)

#while True:

for i in range(0, 500): # 500 is the number of measurements

    # Send data
    message = time.time()
    sent = sock.sendto(str(message), server_address)
