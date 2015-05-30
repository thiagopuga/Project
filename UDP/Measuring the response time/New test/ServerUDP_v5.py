import socket
import sys
import time

# Create a UDP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port
server_address = ('169.254.0.2', 10000)
print('starting up on %s port %s' % server_address, file=sys.stderr)
sock.bind(server_address)

while True:

    data, address = sock.recvfrom(4096)
        
    elapsed_time = time.time() - float(data.decode('utf-8'))

    print('The response time for one measurement was %f seconds' % elapsed_time)
