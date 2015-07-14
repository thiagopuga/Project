import serial
import sys

try:
    serial = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=3)
    
except:
    print "error opening serial port"

resp = ""

try:
    while True:
        while (serial.inWaiting() > 0):
            resp += serial.read()            
            if "\r\n" in resp:
                if "$GPRMC" in resp:
                    data = resp.split(',')
                    if data[2] == 'A':
                        # Get time
                        hour = data[1][0:2]
                        min = data[1][2:4]
                        sec = data[1][4:6]
                        mil = data[1][7:10]
                        time = "%s:%s:%s.%s" % (hour, min, sec, mil)
                        # Get coordinates
                        latitude = data[3]                        
                        hemisphere = data[4]
                        longitude = data[5]
                        side = data[6]
                        coordinates = "%s %s %s %s" % (latitude, hemisphere, longitude, side)
                        # Get date
                        day = data[9][0:2]
                        month = data[9][2:4]
                        year = int(data[9][4:6]) + 2000
                        date = "%s-%s-%d" % (month, day, year)
                        # Print info
                        info = "%s %s %s" % (date, time, coordinates)
                        print info
                resp = ""

except:
    print sys.exc_info()

finally:
    serial.close()
