import RPi.GPIO as GPIO
import serial
import socket
import sys

# 10K Trimpot connected to ADC #0
POTENTIOMETER_ADC = 0;

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
def readAdc(adcNum, clockPin, mosiPin, misoPin, csPin):
        
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
        adcOut >>= 1                    # First bit is "null" so drop it
        
        return adcOut

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverAddress = ("169.254.0.1", 10000)

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
            if "\r\n" in resp:        
                if "$GPRMC" in resp:                        
                    data = resp.split(',')                    
                    if data[2] == 'A':
                            
                        # Read the analog pin
                        trimpot = readAdc(POTENTIOMETER_ADC, SPI_CLK, SPI_MOSI, SPI_MISO, SPI_CS)

                        # Test
                        # print data[1]
                            
                        day = data[9][0:2]
                        month = data[9][2:4]
                        year = int(data[9][4:6]) + 2000
                        date = "%s-%s-%d" % (month, day, year)
                        hour = data[1][0:2]
                        min = data[1][2:4]
                        sec = data[1][4:6]
                        mil = data[1][7:10]
                        
                        time = "%s%s%s%s" % (hour, min, sec, mil)

                        string = time + str(trimpot)

                        # Send data
                        print "Sending", string
                        sent = sock.sendto(string, serverAddress)
                        
                        # Create a log file
                        if date != name:
                            if name != "":
                                file.close()                           
                            name = date
                            file = open(name + ".log", 'w')
                            
                        # Write on log
                        file.write(string + "\n")

                    resp = ""

except:
        print sys.exc_info()#[0]

finally:
        print >>sys.stderr, 'closing socket'
        sock.close()
        print >>sys.stderr, 'closing serial'
        serial.close()
