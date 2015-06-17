import RPi.GPIO as GPIO
import time

# 10K trimpot connected to ADC #0
POTENTIOMETER_ADC = 0;

# Change these as desired - they're the pins connected from the
# SPI port on the ADC to the Cobbler
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
        if ((adcnum > 7) or (adcnum < 0)):
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

while True:
        start = time.time()

        # Read the analog pin
        trimpot = readadc(ADC_CH, SPICLK, SPIMOSI, SPIMISO, SPICS)

        end = time.time()
        print end - start
        print "trimpot ", trimpot

        #time.sleep(0.025)
