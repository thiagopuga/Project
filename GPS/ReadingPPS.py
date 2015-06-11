import RPi.GPIO as GPIO

PPS_PIN = 12

# Setup GPIO using Board numbering
GPIO.setmode(GPIO.BOARD)
GPIO.setup(PPS_PIN, GPIO.IN)

while True:
    if GPIO.input(PPS_PIN):
        print(1)
    else:
        print(0)
