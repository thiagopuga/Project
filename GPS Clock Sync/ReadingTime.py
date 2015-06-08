import RPi.GPIO as GPIO

PPS_PIN = 1

# Set up GPIO using BCM (GPIO) numbering
GPIO.setmode(GPIO.BCM)

GPIO.setup(PPS_PIN, GPIO.IN)

while True:
    if GPIO.input(PPS_PIN):
        print('1 second')
    else:
        print('0')
