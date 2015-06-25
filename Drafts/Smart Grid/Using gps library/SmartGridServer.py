import socket
import struct
import sys

# Create a UDP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port
server_address = ("169.254.0.1", 10001)
print >>sys.stderr, "starting up on %s port %s" % server_address
sock.bind(server_address)

unpacker = struct.Struct("24s I")

while True:
    print >>sys.stderr, "waiting to receive message"
    data, address = sock.recvfrom(unpacker.size)    #sock.recvfrom(4096)
    print >>sys.stderr, "received %s bytes from %s" % (len(data), address)
    print >>sys.stderr, "unpacked", unpacker.unpack(data)
