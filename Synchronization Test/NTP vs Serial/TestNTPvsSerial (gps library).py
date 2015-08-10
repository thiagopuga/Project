import datetime
import gps
import MySQLdb
import RPi.GPIO as GPIO
import socket
import time

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

# Create a UDP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port
server_address = ('169.254.58.49', 10000)
print 'starting up on %s port %s' % server_address
sock.bind(server_address)

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

# Listen on port 2947 (gpsd) of localhost
session = gps.gps('localhost', '2947')
session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)

latitude = 'na' # No answer
longitude = 'na'

# Create a log file    
file = open('Test.log', 'w')

try:
    print 'waiting to receive message'
    data, address = sock.recvfrom(4096)
    print data

    if data == 'start':
            
        print 'sending data...'
        
        while True:
            try:
                report = session.next()        
                # Wait for a 'TPV' report and display the current time
                # To see all report data, uncomment the line below
                # print report
                if report['class'] == 'TPV':
                    if hasattr(report, 'lat'):
                        latitude = str(report.lat)[:11]
                    if hasattr(report, 'lon'):
                        longitude = str(report.lon)[:11]

                # Read ADC
                trimpot = readADC(ADC_CH, SPI_CLK, SPI_MOSI, SPI_MISO, SPI_CS)

                # Read date and time
                date = datetime.datetime.utcnow().strftime('%m%d%Y')
                curTime = datetime.datetime.utcnow().strftime('%H%M%S%f')[:-3]

                # Send to MySQL
                cmd = ('INSERT INTO INFO(ID, Date, Time, Latitude, Longitude, ADC)'
                       'VALUES(%s, %s, %s, %s, %s, %s)')
                data = (RASP_ID, date, curTime, latitude, longitude, trimpot)
                cur.execute(cmd, data)
                con.commit()

                # Write on log
                file.write(curTime + '\n')

                time.sleep(0.5)
               
            except KeyError:
                pass
            except KeyboardInterrupt:
                quit()
            except StopIteration:
                session = None
                print 'GPSD has terminated'
                
except:
    print 'closing socket'
    sock.close()


