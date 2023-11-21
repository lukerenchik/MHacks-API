# -*- coding: utf-8 -*-
"""
Created on Tue Oct  4 12:17:21 2022

@author: Derek Joslin
"""


import TouchScreenInterface as ts
import serial
import time
import matplotlib.pyplot as plt

sensor = ts.TouchScreenInterface("COM7",0)
# =============================================================================
# port = serial.Serial("COM", 57600, timeout=3)
# =============================================================================

time.sleep(1)


# =============================================================================
# 
# port.write(bytearray([30]))
# 
# response = port.read(3)
# =============================================================================



#print(response)

position = sensor.getTouchPosition()


#plt.plot([position[0]],[position[1]],'ro')
#plt.axis([0, 255, 0, 255])
#fig, ax = plt.subplots()

while 1:  
    tic = time.perf_counter()
    

    position = sensor.getTouchPosition()
    print(position)
    #position = sensor.getTouchPosition()
    
    toc = time.perf_counter()
    
    #print(toc - tic)
    #print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
    #print(position)
    #plt.close('all')
    #plt.plot([position[0]],[position[1]],'ro')
    #plt.axis([0, 255, 0, 255])
    #plt.show()
    #plt.close()

    #print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
    
#sensor.close()