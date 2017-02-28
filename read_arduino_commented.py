'''
Written by Jon H. Austad

Python has libraries with higher order functionality for doing anything from
numbercrunching to webdesign and necromancy. Loading all of these all the time
would eat CPU-time and RAM. Therefore, there are only a few essential functions
available all the time, the rest are loaded as needed. The required libraries
for this project are listed below with a short description of their usage.
'''
# Standard libraries
import os                       # interacting with the operating system
import serial                   # reading input serial devices (the arduino)
import time                     # time measurements
import sys                      # command line input

# These two may or may not be installed on your system
import numpy as np              # numbercrunching, arrays, etc.
import pylab as pl              # plotting


'''
The arduino/dallas probe setup is trivially simple:
As long as it has power, it will keep measuring the temperature.
We do not start or stop the arduino as such - much like an old school mercury
thermometer never stops measuring. The arduino sends this data to a serial
device on the raspi - in this case to /dev/ttyACM0
Read more here: https://en.wikipedia.org/wiki/Serial_port

The serial-module allows us to interact with this data stream. The following
block of code contains the incantations required. The number 9600 is the bit
rate in which the arduino sends data to the serial port - that is, 9600 bits
per second.
'''
ser = serial.Serial('/dev/ttyACM0', 9600)

# Log data to file - optional
file = open(sys.argv[1], 'w')

start = time.time()
while True:
    try:
        pstr = ser.readline()
    except KeyboardInterrupt:   # Type Ctrl+C to stop the logging
        break
    try:
        T = float(pstr.split()[0]) # Kelvin
        t = time.time() - start
        raw_t.append(t)
        raw_T.append(T)
        pstr = '%1.8e    %f' %(t, T)
        file.write(pstr + '\n')
        print pstr
    except:
        pass
print '\nLogging completed\n'
file.close()                    # Always close files when you are done


# We delete the first measurements as the data is sometimes borked
del raw_t[0]
del raw_T[0]

'''
Generic function for polynomial fitting
'''
def jpolyfit(X, Y, degree = 2):
    P = np.polyfit(X, Y, deg = degree)
    lbl = 'polyfit: %i. order' %degree
    pl.plot(X, sum([p*X**(degree - i) for i, p in enumerate(P)]), label = lbl)
    return P

# Convert to arrays whenever possible - much more efficient
t = np.array(raw_t)
t -= t[0]                       # t0 = 0, other values adjusted accordingly
T = np.array(raw_T)

pl.plot(t, T, '.-', label = 'rawdata')
jpolyfit(t, T, 6)

pl.grid('on')
pl.legend(loc = 'upper right', shadow = True)
pl.xlabel('t [s]')
pl.ylabel('T [K]')
pl.title('DS18B20')
pl.show()
