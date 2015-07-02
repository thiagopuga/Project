import RPi.GPIO as GPIO
import time

PPS_PIN = 12

# Setup GPIO using Board numbering
GPIO.setmode(GPIO.BOARD)

GPIO.setup(PPS_PIN, GPIO.IN)

while True:
    if GPIO.input(PPS_PIN):
        print "Signal"
        time.sleep(0.0011)
    else:
        print "OK"
