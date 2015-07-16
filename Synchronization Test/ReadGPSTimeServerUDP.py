import serial
import socket
import sys

# Create a UDP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port
server_address = ('169.254.0.2', 10000)
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)

try:
    print >>sys.stderr, 'waiting to receive message'
    data, address = sock.recvfrom(4096)
    print data
    if data == 'start':
        # Connect with serial port
        try:
            serial = serial.Serial('/dev/ttyAMA0', baudrate=9600, timeout=3)    
        except:
            print 'error opening serial port'                
        resp = ''
        fileName = ''
        date = ''
        try:
            while True:
                while (serial.inWaiting() > 0):
                    resp += serial.read()            
                    if '\r\n' in resp:
                        if '$GPRMC' in resp:
                            data = resp.split(',')
                            # Status, V=Navigation receiver warning A=Valid
                            if data[2] == 'A':
                                # Get time
                                hour = data[1][0:2]
                                min = data[1][2:4]
                                sec = data[1][4:6]
                                mil = data[1][7:10]
                                time = '%s%s%s%s' % (hour, min, sec, mil)
                                # Get date
                                day = data[9][0:2]
                                month = data[9][2:4]
                                year = int(data[9][4:6]) + 2000
                                date = '%s-%s-%d' % (month, day, year)
                                string = time
                            else:
                                string = 'no signal'
                            print string
                            # Create a log file    
                            if date != fileName:
                                if fileName != '':
                                    file.close()                           
                                fileName = date
                                file = open('GPS ' + fileName + '.log', 'w')
                            if fileName != '':
                                # Write on log
                                file.write(string + '\n')                            
                        resp = ''                     
        except:
            print sys.exc_info()
        finally:
            print >>sys.stderr, 'closing serial'
            serial.close()
            if fileName != '':
                print >>sys.stderr, 'closing log'
                file.close()            
finally:
    print >>sys.stderr, 'closing socket'
    sock.close() 
