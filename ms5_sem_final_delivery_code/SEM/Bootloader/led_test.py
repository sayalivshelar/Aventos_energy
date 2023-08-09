
###########################################################################
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
from time import sleep # Import the sleep function from the time modul
Restart_led=37

GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD)
GPIO.setup(Restart_led, GPIO.OUT, initial=GPIO.LOW)
GPIO.output(Restart_led, GPIO.HIGH)
sleep(1)
GPIO.output(Restart_led, GPIO.LOW)
sleep(1)
#GPIO.output(Restart_led, GPIO.HIGH)
sleep(5)
GPIO.output(Restart_led, GPIO.LOW)
sleep(1)
GPIO.output(Restart_led, GPIO.HIGH)
sleep(1)
GPIO.output(Restart_led, GPIO.LOW)
sleep(1)
