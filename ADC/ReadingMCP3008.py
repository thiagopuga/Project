import RPi.GPIO as GPIO

# 10k trim pot connected to adc #0
ADC_CH = 0;

# Change these as desired - they're the pins connected from the
# SPI port on the ADC to the Cobbler
SPICLK = 23
SPIMISO = 21
SPIMOSI = 19
SPICS = 24

# Setup GPIO using Board numbering
GPIO.setmode(GPIO.BOARD)

# Set up the SPI interface pins
GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPICS, GPIO.OUT)

# Read SPI data from MCP3008 chip, 8 possible adc's (0 thru 7)
def readadc(adcnum, clockpin, mosipin, misopin, cspin):
        if ((adcnum > 7) or (adcnum < 0)):
                return -1
        GPIO.output(cspin, True)
 
        GPIO.output(clockpin, False)  # Start clock low
        GPIO.output(cspin, False)     # Bring CS low
 
        commandout = adcnum
        commandout |= 0x18  # Start bit + single-ended bit
        commandout <<= 3    # We only need to send 5 bits here
        for i in range(5):
                if (commandout & 0x80):
                        GPIO.output(mosipin, True)
                else:
                        GPIO.output(mosipin, False)
                commandout <<= 1
                GPIO.output(clockpin, True)
                GPIO.output(clockpin, False)
 
        adcout = 0
        # Read in one empty bit, one null bit and 10 ADC bits
        for i in range(12):
                GPIO.output(clockpin, True)
                GPIO.output(clockpin, False)
                adcout <<= 1
                if (GPIO.input(misopin)):
                        adcout |= 0x1
 
        GPIO.output(cspin, True)
        
        adcout >>= 1       # First bit is 'null' so drop it
        return adcout

while True:
        # Read the analog pin
        trim_pot = readadc(ADC_CH, SPICLK, SPIMOSI, SPIMISO, SPICS)
        print "trim_pot:", trim_pot
