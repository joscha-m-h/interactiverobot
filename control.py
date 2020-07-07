#!/usr/bin/env python
# File control.py
# by mjoscha@gmail.com
# Created 28 June 2020

# Requires 
# - Might require a restart for new audio devices
# - Be cautious not to have any player open -> creates resource busy failures
# - Python 3 (for list.copy() command)
# - ffplay or mplayer (sudo apt-get install mplayer)

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

from gpiozero import LED, Button
from pydub import AudioSegment
from pydub import playback

laser = LED(3)
lefteye = LED(20)
movement = Button(16)
laser.off() # legacy
lefteye.on()

random.seed() # Initialize internal state of random number generator based on time
soundsnippetDir = "/home/pi/soundsnippets"



# Time formating: https://docs.python.org/2/library/time.html
now = time.localtime()
now = time.strptime("20 12 06 11:00", "%y %m %d %H:%M")
#now = time.strptime("21 11 07 09:00", "%y %m %d %H:%M")
print(time.strftime("%H:%M %d.%m.%y", now))

def scanDirectory(path):
    #print("Scanning " + path)
    for dirpath, dirnames, filenames in os.walk(path):
        fileweights = filenames.copy()
        for index, filename in enumerate(filenames):
            try:
                weight = int(filename[0])
            except:
                weight = 5
            fileweights[index] = weight
                
            #print("filename: " + filename)
        return(fileweights, filenames, dirpath)

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
    
def pickRandom(selectionValues): # selection values is a tuple containing [0] = weights, [1] = filenames, [2] = path
    fileName = random.choices(selectionValues[1], weights = selectionValues[0]) # Returns a list with one element
    fullpath = os.path.join(selectionValues[2], fileName[0])
    print(fileName)
    print(selectionValues[2])
    return(fullpath)

#while True:
#    print("Wait for motion")
#    pir.wait_for_motion()
#    print("Motion detected")
#    time.sleep(1)

seasonSpecific, daySpecific, timeSpecific, generic = findFiles(now)

countSeason = len(seasonSpecific[0])
countDay = len(daySpecific[0])
countTime = len(timeSpecific[0])
countGeneric = len(generic[0])

# Decide which song category to play
if getRandom(50):
    print("Only flashing eyes")
    sound = "Silence" # Random choices returns a list, so we make this a list too
elif countSeason > 0  and getRandom(30):
    print("Playing seasonal")
    sound = pickRandom(seasonSpecific)
elif countDay > 0 and getRandom(70):
    print("Playing day specific")
    sound = pickRandom(daySpecific)
elif countTime > 0 and getRandom(30):
    print("Playing time specific")
    sound = pickRandom(timeSpecific)
else:
    print("Playing generic")
    sound = pickRandom(generic)


if sound == "Silence":
    print("SILENCE - Flashing eyes only")
else: 
    print("PLAYING SOUND: " + sound)
    sound = "/home/pi/Downloads/test.mp3" # TODO DELETE
    # Console command ffplay (does not stop automatically)
    # ffplay -nodisp -hide_banner ../../Downloads/test.mp3 
    #command = "ffplay -nodisp -hide_banner"
    
    # Console command mplayer (works just fine)
    # mplayer  ../../Downloads/test.mp3 
    command = "mplayer"  
    os.system(command + " "+ sound)
    
