import socket
import sys

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address1 = ('169.254.0.2', 10000)
server_address2 = ('169.254.0.3', 10000)

message = 'stop'

try:
    # Send data
    print >>sys.stderr, 'sending %s' % message
    sent = sock.sendto(message, server_address1)
    sent = sock.sendto(message, server_address2)
    
finally:
    print >>sys.stderr, 'closing socket'
    sock.close()
