#!/usr/bin/env python
# File control.py
# by mjoscha@gmail.com
# Created 28 June 2020


# TODO
# - Create thread for playing sound
# - Create thread for blinking with eyes
# - Test motion sensor
# - Modify category selection probabilities to consider the number of songs in playlist?

# Readme
# Encoding of soundsnippet folder in /home/pi/soundsnippets
# - day - create folder with date in following writing: MMDD
#       - will be played every year on that day only
#
# - seasonal - create folder with following writing MM
#            - will be played any year in this month
#
# - time - create folder with following writing HH
#        - will be played at this hour and the subsequent minutes till full next hour
#
# - FILENAMES
# - Put any integer 0-9 as first character in file name
#    0 - Play extremely rarely
#    5 - Play average (default)
#    9 - Play frequently


import time
import datetime
import random
import os

random.seed() # Initialize internal state of random number generator based on time
soundsnippetDir = "/home/pi/soundsnippets"



# Time formating: https://docs.python.org/2/library/time.html
now = time.localtime()
now = time.strptime("20 12 06 11:00", "%y %m %d %H:%M")
print(now)

def scanDirectory(path):
    print("Scanning " + path)
    for files in os.walk(path):
        for filename in files:
            print(filename)
            #print(os.path.join(path, filename))


# Call with getRandom(70) to get True in 70% of cases
def getRandom(percentage):
    randomNumber = random.randint(1, 100)
    if randomNumber <= percentage:
        return True
    else:
        return False
        
def findFiles(now):
    print("Searching directories")
    seasonT = time.strftime("%m", now)
    dayT = time.strftime("%m%d", now)
    timeT = time.strftime("%H%M", now)
    
    scanDirectory(os.path.join(soundsnippetDir, "season", seasonT))
    scanDirectory(os.path.join(soundsnippetDir, "day", dayT))
    scanDirectory(os.path.join(soundsnippetDir, "time", timeT))

    # TEMP
    seasonSpecific = True
    daySpecific = True
    timeSpecific = True


    return((seasonSpecific, daySpecific, timeSpecific))
    
def getWeightings():
    print("Calculating weighted vector of files")
    

    
    


seasonSpecific, daySpecific, timeSpecific = findFiles(now)

# Decide which song category to play
if getRandom(50):
    print("Only flashing eyes")
if seasonSpecific  and getRandom(30):
    print("Playing seasonal")
elif daySpecific and getRandom(50):
    print("Playing day specific")
elif timeSpecific and getRandom(30):
    print("Playing time specific")
else:
    print("Playing generic")

