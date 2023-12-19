#!/usr/bin/env python3
import time
import sys
import os
import numpy as np
from matplotlib import animation as animation, pyplot as plt

# Set path to AS7341 library
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pispec/lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

from waveshare_AS7341 import AS7341

# Declare globals
fig = plt.figure(num=" ", figsize = (10, 6))
data = [10, 20, 30, 40, 50, 60, 70, 80]
colors = ['violet', 'indigo', 'blue', 'cyan', 'green', 'yellow', 'orange', 'red', ]
wavelengths = [418.75, 456.25, 493.75, 531.25, 568.75, 606.25, 643.75, 681.25]
bars = plt.bar(wavelengths, data, width=32, color=colors)
obj = AS7341.AS7341()

# Animation fuction to update bar graph with sensor data
def animate(frame):
    global bars
    intensity = 0
    match frame:
        case 0:
            intensity = obj.channel1*100/65535
        case 1:
            intensity = obj.channel2*100/65535
        case 2:
            intensity = obj.channel3*100/65535
        case 3:
            intensity = obj.channel4*100/65535
        case 4:
            intensity = obj.channel5*100/65535
        case 5:
            intensity = obj.channel6*100/65535
        case 6:
            intensity = obj.channel7*100/65535
        case 7:
            intensity = obj.channel8*100/65535  
            # Perform next measurement 
            obj.AS7341_startMeasure(0)
            obj.AS7341_ReadSpectralDataOne() 
            obj.AS7341_startMeasure(1)
            obj.AS7341_ReadSpectralDataTwo()        
        case _:
            intesity = 0

    bars[frame].set_height(intensity)

# Set animation function to figure
ani = animation.FuncAnimation(fig, animate, frames=len(data))    

def main():
    # Setup AS7341
    obj.measureMode = 0
    obj.AS7341_ATIME_config(100)
    obj.AS7341_ASTEP_config(999)
    obj.AS7341_AGAIN_config(6)
    #obj.AS7341_EnableLED(True)      #LED Enable
    #obj.AS7341_ControlLed(True,10)
    #time.sleep(5)
    #obj.AS7341_EnableLED(False)     #LED Disable

    # Take first sensor measurements
    obj.AS7341_startMeasure(0)
    obj.AS7341_ReadSpectralDataOne()
    obj.AS7341_startMeasure(1)
    obj.AS7341_ReadSpectralDataTwo() 

    # Setup and display bar graph
    plt.title("AS7341 Spectrograph")
    plt.xlabel("Wavelength (nm)")
    plt.ylabel("Intensity")
    plt.xlim(400, 700)
    plt.ylim(0,100)
    plt.show()    

if __name__ == "__main__":
    main()