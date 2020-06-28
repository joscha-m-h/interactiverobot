#!/usr/bin/env python
# File control.py
# by mjoscha@gmail.com
# Created 28 June 2020


# TODO
# - Modify category selection probabilities to consider the number of songs in playlist?

import time
import datetime
import random

random.seed() # Initialize internal state of random number generator based on time

now = time.localtime()
print(now)


# Call with getRandom(70) to get True in 70% of cases
def getRandom(percentage):
    randomNumber = random.randint(1, 100)
    if randomNumber <= percentage:
        return True
    else:
        return False

seasonalSpecific = True
daySpecific = True
timeSpecific = True

# Decide which song category to play
if seasonalSpecific  and getRandom(30):
    print("Playing seasonal")
elif daySpecific and getRandom(50):
    print("Playing day specific")
elif timeSpecific and getRandom(30):
    print("Playing time specific")
else:
    print("Playing generic")

