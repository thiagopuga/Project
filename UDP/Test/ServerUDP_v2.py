import socket
import sys
import time

NO_CONNECTIONS = 100

# Create a UDP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port
server_address = ('169.254.0.1', 10000)
print('starting up on %s port %s' % server_address, file=sys.stderr)
sock.bind(server_address)

while True:    
    total_elapsed_time = 0

    for i in range(0, NO_CONNECTIONS):        
        data, address = sock.recvfrom(4096)

        #print('received "%s"' % data.decode('utf-8'), file=sys.stderr)
        
        elapsed_time = time.time() - float(data.decode('utf-8'))
        total_elapsed_time = total_elapsed_time + elapsed_time

    print('The total response time was %f seconds' % total_elapsed_time)
