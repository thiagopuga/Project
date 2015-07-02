import socket
import sys

# Create a UDP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port
server_address = ("169.254.0.1", 10000)
print >>sys.stderr, "starting up on %s port %s" % server_address
sock.bind(server_address)

fileName = ""

try:
    while True:
        print >>sys.stderr, "waiting to receive message"
        data, address = sock.recvfrom(4096)
        print >>sys.stderr, "received %s bytes from %s" % (len(data), address)
        # Split data
        resp = data.split(',')
        date = resp[0]
        string = resp[1]    
        # Create a log file    
        if date != fileName:
            if fileName != "":
                file.close()                           
            fileName = date
            file = open(fileName + ".log", 'a')
        # Write on log
        file.write(string + "\n")

finally:
    print >>sys.stderr, 'closing socket'
    sock.close()
    print >>sys.stderr, 'closing log'
    file.close()
