import socket
import sys
import time

NUMBER_MEASUREMENTS = 100

# Create a UDP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port
server_address = ('169.254.0.1', 10000)
print('starting up on %s port %s' % server_address, file=sys.stderr)
sock.bind(server_address)

while True:
    
    sum_elapsed_time = 0

    for i in range(0, NUMBER_MEASUREMENTS):        
        data, address = sock.recvfrom(4096)
        
        elapsed_time = time.time() - float(data.decode('utf-8'))
        sum_elapsed_time = sum_elapsed_time + elapsed_time

    total_elapsed_time = sum_elapsed_time / NUMBER_MEASUREMENTS

    print('The response time for %d measurements was %f seconds' % (NUMBER_MEASUREMENTS, total_elapsed_time))
