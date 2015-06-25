import serial
import sys

try:
    serial = serial.Serial("/dev/ttyAMA0", baudrate=9600)
    
except:
    print "Error opening serial port."

resp = ""
name = ""

try:
    while True:
        while (serial.inWaiting() > 0):
            resp += serial.read()

            #print resp
            #print ""

            
            if "\r\n" in resp:
                if "$GPGGA" in resp:
                    data = resp.split(',')
                    hour = data[1][0:2]
                    min = data[1][2:4]
                    sec = data[1][4:6]
                    mil = data[1][7:10]
                    time = "%s:%s:%s.%s" % (hour, min, sec, mil)
                    print time
                elif "$GPRMC" in resp:
                    data = resp.split(',')
                    day = data[9][0:2]
                    month = data[9][2:4]
                    year = int(data[9][4:6]) + 2000
                    date = "%s-%s-%d" % (month, day, year)
                    hour = data[1][0:2]
                    min = data[1][2:4]
                    sec = data[1][4:6]
                    mil = data[1][7:10]
                    time = "%s:%s:%s.%s" % (hour, min, sec, mil)
                    dateTime = "%s %s" % (date, time)
                    print time #dateTime
                resp = ""

except:
    print sys.exc_info()

finally:
    serial.close()
