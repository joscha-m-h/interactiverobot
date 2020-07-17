#!/usr/bin/env python
# File control.py
# by mjoscha@gmail.com
# Created 28 June 2020

# Features
# - Eyes flashing with Gaussian probabilities ;)
# - Season, Day and Time-specific sounds
# - Sound specific playback probabilities
# - 

# Requires 
# - Might require a restart for new audio devices
# - Be cautious not to have any player open -> creates resource busy failures
# - Python 3 (for list.copy() command)
# - ffplay or mplayer (sudo apt-get install mplayer)

# TODO
# - what happens if invalid sound file
# - Port everything to old Raspi
# - Solder LEDs and PIR
# - Create carton prototype
# - Anonymize (Remove Cookies / passwords / login from chrome, remove truewheelz code, remove github private/public keys)

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
#    1 - Play extremely rarely
#    5 - Play average (default)
#    9 - Play frequently

### IMPORTS ############################################################

import time
import datetime
import random
import os

from gpiozero import LED, Button, MotionSensor
from threading import Thread

### INITIALIZATION #####################################################
laser = LED(3)
lefteye = LED(20)
righteye = LED(21)
pir = MotionSensor(16, pull_up = False, threshold=0.7)
#movement = Button(16)
laser.off() # legacy
lefteye.on() # shows that SW is running after bootup

random.seed() # Initialize internal state of random number generator based on time
soundsnippetDir = "/home/pi/soundsnippets"


### THREADS ############################################################

class flashingLed():
    def __init__(self, ledid):
        self._running = True
        self.ledid = ledid
        
    def stop(self):
        self._running = False
        
    def start(self):
        while self._running:
            self.ledid.on()
            time.sleep(abs(random.gauss(.5, .75)))
            self.ledid.off()
            time.sleep(abs(random.gauss(.2, .4)))

### FUNCTIONS ##########################################################

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
    weekdayT = time.strftime("%w %A", now).lower()
    
    seasonSpecific = scanDirectory(os.path.join(soundsnippetDir, "season", seasonT))
    weekdaySpecific = scanDirectory(os.path.join(soundsnippetDir, "weekday", weekdayT))
    daySpecific = scanDirectory(os.path.join(soundsnippetDir, "day", dayT))
    timeSpecific = scanDirectory(os.path.join(soundsnippetDir, "time", timeT))
    generic = scanDirectory(os.path.join(soundsnippetDir, "generic"))
    return((seasonSpecific, weekdaySpecific, daySpecific, timeSpecific, generic))
    
def pickRandom(selectionValues): # selection values is a tuple containing [0] = weights, [1] = filenames, [2] = path
    fileName = random.choices(selectionValues[1], weights = selectionValues[0]) # Returns a list with one element
    fullpath = os.path.join(selectionValues[2], fileName[0])
    print(fileName)
    print(selectionValues[2])
    return(fullpath)
    
# Custom length function
def lenC(thing):
    if thing is None:
        return 0
    else:
        return len(thing[0])
    
### MAIN CODE ##########################################################

while True:
    print("Wait for motion")
    pir.wait_for_motion()
    print("Motion detected")
    # Time formating: https://docs.python.org/2/library/time.html
    now = time.localtime()
    #now = time.strptime("20 12 06 11:00", "%y %m %d %H:%M")
    #now = time.strptime("21 11 07 09:00", "%y %m %d %H:%M")
    print(time.strftime("%H:%M %d.%m.%y", now))

    seasonSpecific, weekdaySpecific, daySpecific, timeSpecific, generic = findFiles(now)

    leftClass = flashingLed(lefteye)
    rightClass = flashingLed(righteye)

    print(seasonSpecific)
    print(weekdaySpecific)

    countSeason = lenC(seasonSpecific)
    countWeekday = lenC(weekdaySpecific)
    countDay = lenC(daySpecific)
    countTime = lenC(timeSpecific)
    countGeneric = lenC(generic)

    # Decide which song category to play
    if getRandom(70):
        print("Only flashing eyes")
        sound = "Silence" # Random choices returns a list, so we make this a list too
    elif countSeason > 0  and getRandom(30):
        print("Playing seasonal")
        sound = pickRandom(seasonSpecific)
    elif countWeekday > 0  and getRandom(20):
        print("Playing weekday")
        sound = pickRandom(weekdaySpecific)
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
        
        threadLeft = Thread(target = leftClass.start)
        threadRight = Thread(target = rightClass.start)

        threadLeft.start()
        threadRight.start()

        time.sleep(2) # Flashing eyes for 2 seconds
        
        leftClass.stop()
        rightClass.stop()
        
    else: 
        print("PLAYING SOUND: " + sound)
        #sound = "/home/pi/Downloads/test.mp3" # TODO DELETE
        # Console command ffplay (does not stop automatically)
        # ffplay -nodisp -hide_banner ../../Downloads/test.mp3 
        #command = "ffplay -nodisp -hide_banner"
        
        # Console command mplayer (works just fine)
        # mplayer  ../../Downloads/test.mp3 
        command = "mplayer"  

        threadLeft = Thread(target = leftClass.start)
        threadRight = Thread(target = rightClass.start)

        threadLeft.start()
        threadRight.start()
        
        os.system(command + " '"+ sound + "'")

        with open("log.txt", "a") as myfile:
            myfile.write(time.strftime("%H:%M %d.%m.%y", now) + " - " + sound + "\n")
                
        
        leftClass.stop()
        rightClass.stop()

    print("FINISHED - Sleep 1s and go again")
    time.sleep(1)
