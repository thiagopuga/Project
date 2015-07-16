import datetime
import time
import socket
import sys

# Create a UDP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port
server_address = ('169.254.0.3', 10000)
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)

try:
    print >>sys.stderr, 'waiting to receive message'
    data, address = sock.recvfrom(4096)
    print data
    if data == 'start':
        fileName = ''
        try:
            while True:
                resp = datetime.datetime.utcnow().strftime('%m-%d-%Y,%H%M%S%f')        
                data = resp.split(',')
                date = data[0]
                curTime = data[1]
                print curTime
                # Create a log file    
                if date != fileName:
                        if fileName != '':
                                file.close()                           
                        fileName = date
                        file = open('OS ' + fileName + '.log', 'w')
                # Write on log
                file.write(curTime + '\n')
                time.sleep(0.1)    # Sleep for 100 milliseconds
        except:
            print sys.exc_info()
        finally:
            if fileName != '':
                print >>sys.stderr, 'closing log'
                file.close()
finally:
    print >>sys.stderr, 'closing socket'
    sock.close() 
