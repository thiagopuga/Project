import RPi.GPIO as GPIO
import serial
import socket
import sys
import time

# Set warnings off
GPIO.setwarnings(False)

# ID
RASP_ID = '1'

# Time sources
GPS = 'G'
OS = 'O'

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

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverAddress = ('169.254.0.1', 10000)

# Connect with serial port
try:
    serial = serial.Serial('/dev/ttyAMA0', baudrate=9600)
except:
    print 'error opening serial port'

resp = ''

try:
    while True:
        while (serial.inWaiting() > 0):
            resp += serial.read()          
            if '\r\n' in resp:        
                if '$GPRMC' in resp:
                    # Read the analog pin
                    trimpot = readADC(ADC_CH, SPI_CLK, SPI_MOSI, SPI_MISO, SPI_CS)
                    data = resp.split(',')
                    # Status, V=Navigation receiver warning A=Valid
                    if data[2] == 'A':
                            time = data[1]
                            latitude = data[3]
                            hemisphere = data[4]
                            longitude = data[5]
                            side = data[6]
                            day = data[9][0:2]
                            month = data[9][2:4]
                            year = int(data[9][4:6]) + 2000
                            date = '%s-%s-%d' % (month, day, year)
                            # Create string
                            string = date + ',' + RASP_ID + GPS + time + latitude + hemisphere + longitude + side + str(trimpot)
                            # Remove dots
                            string = string.replace('.', '')
                    else:
                            date = time.strftime('%m-%d-%Y')
                            time = time.strftime('%H%M%S')
                            # Create string
                            string = date + ',' + RASP_ID + OS + time + str(trimpot)
                    # Send data
                    print 'sending', string
                    sent = sock.sendto(string, serverAddress)                            
                resp = ''

except:
    print sys.exc_info()
        
finally:
    print >>sys.stderr, 'closing socket'
    sock.close()
    print >>sys.stderr, 'closing serial'
    serial.close()
    GPIO.cleanup()
