import RPi.GPIO as GPIO

class MCP3008Controller(object):        

    def getValue(self, adcNum, clockPin, mosiPin, misoPin, csPin):
        
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
