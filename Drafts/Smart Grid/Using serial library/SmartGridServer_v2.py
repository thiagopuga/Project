import socket
import struct
import sys

# Create a UDP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port
server_address = ("169.254.0.1", 10000)
print >>sys.stderr, "starting up on %s port %s" % server_address
sock.bind(server_address)

#unpacker = struct.Struct("12s I")

while True:
    print >>sys.stderr, "waiting to receive message"
    data, address = sock.recvfrom(4096)
    print >>sys.stderr, "received %s bytes from %s" % (len(data), address)

    hour = data[0:2]
    min = data[2:4]
    sec = data[4:6]
    mil = data[6:9]
    time = "%s:%s:%s.%s" % (hour, min, sec, mil)
    trimpot = data[9:13]
    data = time + " " + trimpot
    print >>sys.stderr, data
