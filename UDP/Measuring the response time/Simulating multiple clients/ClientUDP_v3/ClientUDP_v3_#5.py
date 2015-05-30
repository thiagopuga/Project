import socket
import sys
import time

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ('169.254.0.2', 10000)

while True:

    # Send data
    message = time.time()
    sent = sock.sendto(str(message).encode(), server_address)
