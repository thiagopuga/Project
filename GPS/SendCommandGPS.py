import serial
import sys

try:
    serial = serial.Serial('/dev/ttyAMA0', baudrate=9600, timeout=3)
    
except:
    print 'error opening serial port'

resp = ''

try:
    # PMTK_SET_NMEA_UPDATE_10HZ
    serial.write('$PMTK220,100*2F\r\n')
    
    # PMTK_SET_NMEA_OUTPUT_RMCONLY
    serial.write('$PMTK314,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0*29\r\n')

    # PMTK_SET_NMEA_OUTPUT_ALLDATA
    #serial.write('$PMTK314,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0*28\r\n')    
    
    print 'OK'
    
    while True:
        while (serial.inWaiting() > 0):
            resp += serial.read()            
            if '\r\n' in resp:
                print resp
                resp = ''

except:
    print sys.exc_info()

finally:
    serial.close()
