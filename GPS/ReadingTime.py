import RPi.GPIO as GPIO
import threading
from gps import *

PPS = 12

class GPS_Controller(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.gpsd = gps(mode=WATCH_ENABLE)  # Starting the stream of info
        self.running = False
    
    def run(self):
        self.running = True
        while self.running:
            # Grab each set of gpsd info to clear the buffer
            self.gpsd.next()

    def stopController(self):
        self.running = False

    @property
    def fix(self):
        return self.gpsd.fix

# Setup GPIO using Board numbering
GPIO.setmode(GPIO.BOARD)

GPIO.setup(PPS, GPIO.IN)

# create the controller
gpsc = GPS_Controller()

try:
    # Start controller
    gpsc.start()
    
    while True:
        if GPIO.input(PPS):
            print 'Time: ', gpsc.fix.time

finally:
    gpsc.stopController()
    
    # Wait for the tread to finish
    gpsc.join()
  
print 'Done!'
