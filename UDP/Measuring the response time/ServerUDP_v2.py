import socket
import sys
import time

# Create a UDP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port
server_address = ("169.254.0.1", 10000)
print >>sys.stderr, "starting up on %s port %s" % server_address
sock.bind(server_address)

while True:
    
    data, address = sock.recvfrom(4096)
    elapsed_time = time.time() - float(data)
    print >>sys.stderr, "The response time was %d seconds" % elapsed_time
