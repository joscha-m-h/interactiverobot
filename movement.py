import time
from gpiozero import Button



from gpiozero import MotionSensor

pir = MotionSensor(16, pull_up = False, threshold=0.7)
pir.wait_for_motion(timeout = 10) # wait X seconds
print("Motion detected!")
pir.wait_for_no_motion(timeout = 10) # wait X seconds
print("No motion detected!")
