import serial
import sys

START_TIME = 215500000
END_TIME = 220000000

def readGPS():
    resp = ""
    while True:
        while (serial.inWaiting() > 0):
            resp += serial.read()          
            if "\r\n" in resp:        
                if "$GPRMC" in resp:                    
                    data = resp.split(',')
                    # Status, V=Navigation receiver warning A=Valid
                    if data[2] == 'A':                        
                        # Get time
                        hour = data[1][0:2]
                        min = data[1][2:4]
                        sec = data[1][4:6]
                        mil = data[1][7:10]
                        time = "%s%s%s%s" % (hour, min, sec, mil)
                        # Get date
                        day = data[9][0:2]
                        month = data[9][2:4]
                        year = int(data[9][4:6]) + 2000
                        date = "%s-%s-%d" % (month, day, year)
                        string = date + "," + time
                    else:
                        string = "no signal"
                    return string
                resp = ""

# Connect with serial port
try:
    serial = serial.Serial("/dev/ttyAMA0", baudrate=9600)
except:
    print "error opening serial port"

fileName = ""

try:
    string = readGPS()
    while string == "no signal":
        string = readGPS()
    data = string.split(',')
    time = data[1]
    while int(time) < START_TIME:
        string = readGPS()
        if string != "no signal":
            data = string.split(',')
            time = data[1]
    
    while int(time) <= END_TIME:
        string = readGPS()
        if string != "no signal":
            data = string.split(',')
            date = data[0]
            time = data[1]
            print time
            string = time
        # Create a log file    
        if date != fileName:
            if fileName != "":
                    file.close()                           
            fileName = date
            file = open(fileName + ".log", 'a')
        # Write on log
        file.write(string + "\n")

except:
    print sys.exc_info()
        
finally:
    print >>sys.stderr, 'closing serial'
    serial.close()
