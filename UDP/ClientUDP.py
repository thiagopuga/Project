import socket
import sys

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ('169.254.0.2', 10000)

try:

    # Send data
    message = 'This is the message. It will be repeated.'
    print('sending "%s"' % message, file=sys.stderr)
    sent = sock.sendto(message.encode(), server_address)

    # Receive response
    print('waiting to receive', file=sys.stderr)
    data, server = sock.recvfrom(4096)
    print('received "%s"' % data.decode('utf-8'), file=sys.stderr)

finally:
    print('closing socket', file=sys.stderr)
    sock.close()
