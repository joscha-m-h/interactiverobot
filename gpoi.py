import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(20, GPIO.OUT)
print "LED on "
GPIO.output(20, GPIO.HIGH)
time.sleep(1)
print("LED off")
GPIO.output(20, GPIO.LOW)

button = Button(16, pull_up = False)
time.sleep(1)
button.wait_for_press()
print("The button was pressed!")
time.sleep(1)
button.wait_for_press()
print("The button was pressed!")
