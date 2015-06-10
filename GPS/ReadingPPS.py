import RPi.GPIO as GPIO

PPS = 12

# Setup GPIO using Board numbering
GPIO.setmode(GPIO.BOARD)

GPIO.setup(PPS, GPIO.IN)

while True:
    
    if GPIO.input(PPS):
        print(1)
    else:
        print(0)
