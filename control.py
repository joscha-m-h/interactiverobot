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

from gpiozero import LED
LED(3).off()

random.seed() # Initialize internal state of random number generator based on time
soundsnippetDir = "/home/pi/soundsnippets"



# Time formating: https://docs.python.org/2/library/time.html
now = time.localtime()
now = time.strptime("20 12 06 11:00", "%y %m %d %H:%M")
#now = time.strptime("21 11 07 09:00", "%y %m %d %H:%M")
print(time.strftime("%H:%M %d.%m.%y", now))

def scanDirectory(path):
    print("Scanning " + path)
    for dirpath, dirnames, filenames in os.walk(path):
        # Following loop only required if weightings should be read
        for filename in filenames:
            print("filename: " + filename)
            #print(os.path.join(path, filename))
        return(filenames)

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
    
    seasonSpecific = scanDirectory(os.path.join(soundsnippetDir, "season", seasonT))
    daySpecific = scanDirectory(os.path.join(soundsnippetDir, "day", dayT))
    timeSpecific = scanDirectory(os.path.join(soundsnippetDir, "time", timeT))
    generic = scanDirectory(os.path.join(soundsnippetDir, "generic"))
    return((seasonSpecific, daySpecific, timeSpecific, generic))
    
def getWeightings():
    print("Calculating weighted vector of files")
    
seasonSpecific, daySpecific, timeSpecific, generic = findFiles(now)


print(seasonSpecific)
countSeason = len(seasonSpecific)
countDay = len(daySpecific)
countTime = len(timeSpecific)
countGeneric = len(generic)

# Decide which song category to play
if getRandom(50):
    print("Only flashing eyes")
    sound = "Silence"
elif countSeason > 0  and getRandom(30):
    print("Playing seasonal")
    sound = seasonSpecific[random.randint(0, countSeason-1)]
elif countDay > 0 and getRandom(70):
    print("Playing day specific")
    sound = daySpecific[random.randint(0, countDay-1)]
elif countTime > 0 and getRandom(30):
    print("Playing time specific")
    sound = timeSpecific[random.randint(0, countTime-1)]
else:
    print("Playing generic")
    sound = generic[random.randint(0, countGeneric-1)]


print("PLAYING SOUND: " + sound)
