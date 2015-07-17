import serial
import sys

# Connect with serial port
try:
    serial = serial.Serial('/dev/ttyAMA0', baudrate=9600, timeout=3)    
except:
    print 'error opening serial port'                

resp = ''

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
                        string = '%s:%s:%s.%s' % (hour, min, sec, mil)
                    else:
                        string = 'no signal'
                    print string               
                resp = ''
except:
    print sys.exc_info()
finally:
    print >>sys.stderr, 'closing serial'
    serial.close()
