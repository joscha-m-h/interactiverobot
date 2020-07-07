import time
from gpiozero import Button



from gpiozero import MotionSensor

pir = MotionSensor(16, pull_up = False, threshold=0.7)

#while True:
#    print("VAlue: " + str(pir.value))
#    time.sleep(1)
    
    
while True:
    print("Wait for motion")
    pir.wait_for_motion()
    print("Motion detected")
    time.sleep(1)

#pir.wait_for_motion(timeout = 10) # wait X seconds
#print("Motion detected!")
#pir.wait_for_no_motion(timeout = 10) # wait X seconds
#print("No motion detected!")
