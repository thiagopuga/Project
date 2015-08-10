import datetime
import MySQLdb
import RPi.GPIO as GPIO
import serial
import sys

# Set warnings off
GPIO.setwarnings(False)

# Raspberry Pi's ID
RASP_ID = 1

# ADC channel
ADC_CH = 0;

# SPI interface pins connected to ADC
SPI_CLK = 23
SPI_MISO = 21
SPI_MOSI = 19
SPI_CS = 24

# Setup GPIO using Board numbering
GPIO.setmode(GPIO.BOARD)

# Set up the SPI interface pins
GPIO.setup(SPI_MOSI, GPIO.OUT)
GPIO.setup(SPI_MISO, GPIO.IN)
GPIO.setup(SPI_CLK, GPIO.OUT)
GPIO.setup(SPI_CS, GPIO.OUT)

# Read SPI data from MCP3008 chip, 8 possible ADC's (0 thru 7)
def readADC(adcNum, clockPin, mosiPin, misoPin, csPin):
        
        if ((adcNum > 7) or (adcNum < 0)):
                return -1
        GPIO.output(csPin, True)
        GPIO.output(clockPin, False)    # Start clock low
        GPIO.output(csPin, False)       # Bring CS low
        commandOut = adcNum
        commandOut |= 0x18              # Start bit + single-ended bit
        commandOut <<= 3                # We only need to send 5 bits here
        
        for i in range(5):
                if (commandOut & 0x80):
                        GPIO.output(mosiPin, True)
                else:
                        GPIO.output(mosiPin, False)
                commandOut <<= 1
                GPIO.output(clockPin, True)
                GPIO.output(clockPin, False)

        adcOut = 0
        
        # Read in one empty bit, one null bit and 10 ADC bits
        for i in range(12):
                GPIO.output(clockPin, True)
                GPIO.output(clockPin, False)
                adcOut <<= 1
                if (GPIO.input(misoPin)):
                        adcOut |= 0x1
                        
        GPIO.output(csPin, True)
        adcOut >>= 1                    # First bit is 'null' so drop it
        
        return adcOut

try:
    print 'connecting to database...'
    con = MySQLdb.connect(host='mydbinstance.cmkub5asq0w1.us-west-2.rds.amazonaws.com',
                          port=3306,
                          user='awsuser',
                          passwd='MyDatabase',
                          db='SPI');
    cur = con.cursor()

except:
    print 'error opening database'

print 'connected to the database'

try:
    print 'opening serial port...'
    serial = serial.Serial('/dev/ttyAMA0', baudrate=9600, timeout=3)
    
except:
    print 'error opening serial port'

print 'connected to the serial port'

resp = ''

latitude = 'no signal'
hemisphere = 'n'
longitude = 'no signal'
side = 'n'

print 'sending data...'

try:
    while True:
        while (serial.inWaiting() > 0):
            resp += serial.read()            
            if '\r\n' in resp:
                if '$GPRMC' in resp:                        
                    data = resp.split(',')
                    if data[2] == 'A':
                        # Set reference
                        reference = 'GPS'
                        # Get time
                        hour = data[1][0:2]
                        min = data[1][2:4]
                        sec = data[1][4:6]
                        mil = data[1][7:10]
                        time = '%s%s%s%s' % (hour, min, sec, mil)
                        # Get coordinates
                        latitude = data[3]                        
                        hemisphere = data[4]
                        longitude = data[5]
                        side = data[6]
                        # Get date
                        day = data[9][0:2]
                        month = data[9][2:4]
                        year = int(data[9][4:6]) + 2000
                        date = '%s%s%d' % (month, day, year)                        
                    if data[2] == 'V':
                        # Set reference
                        reference = 'OS'
                        # Get date and time from Linux
                        date = datetime.datetime.utcnow().strftime('%m%d%Y')
                        time = datetime.datetime.utcnow().strftime('%H%M%S%f')[:-3]
                        # Send the last location from the GPS
                    # Read ADC
                    trimpot = readADC(ADC_CH, SPI_CLK, SPI_MOSI, SPI_MISO, SPI_CS)
                    # Send to MySQL
                    cmd = ('INSERT INTO INFO(ID, Reference, Date, Time, Latitude, Hemisphere, Longitude, Side, ADC)'
                           'VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)')
                    info = (RASP_ID, reference, date, time, latitude, hemisphere, longitude, side, trimpot)
                    cur.execute(cmd, info)
                    con.commit()
                resp = ''

except:
    print sys.exc_info()

finally:
    serial.close()
