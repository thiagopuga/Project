import socket
import sys

# Create a UDP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port
server_address = ('169.254.0.1', 10000)
print('starting up on %s port %s' % server_address, file=sys.stderr)
sock.bind(server_address)

while True:
    print('waiting to receive message', file=sys.stderr)
    data, address = sock.recvfrom(4096)

    print('received %s bytes from %s' % (len(data), address), file=sys.stderr)
    print('received "%s"' % data.decode('utf-8'), file=sys.stderr)
    
    if data:
        sent = sock.sendto(data, address)
        print('sent %s bytes back to %s' % (sent, address), file=sys.stderr)
