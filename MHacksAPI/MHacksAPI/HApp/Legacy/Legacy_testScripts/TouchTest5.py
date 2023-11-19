# -*- coding: utf-8 -*-
"""
Created on Mon Oct 24 15:13:18 2022

@author: Derek Joslin
"""

import TouchScreenInterface as ts
import time
import matplotlib.pyplot as plt

sensor = ts.TouchScreenInterface("COM7",0)

getVerticalPositionCommand   = [1, 2, 3, 0, 2, 3, 0, 3, 2, 1]
getHorizontalPositionCommand   = [1, 2, 3, 0, 2, 2, 0, 3, 2, 1]
getVerticalPositionCommand = bytearray(getVerticalPositionCommand)
getHorizontalPositionCommand = bytearray(getHorizontalPositionCommand)

positionList = []
timeList = []

period = 0.00135

#tic = time.perf_counter()
while 1:    
    tic = time.perf_counter()
    sensor.port.write(getVerticalPositionCommand)
    
    toc = time.perf_counter()
    while (toc - tic) < period:
        toc = time.perf_counter()
        
    sensor.port.write(getHorizontalPositionCommand)   
    
    #time.sleep(0.00005)
    tic = time.perf_counter()
    toc = time.perf_counter()
    while (toc - tic) < period:
        toc = time.perf_counter()
    #response = sensor.port.read(20)
    #verticalPosition = 255  - response[-14]
    #horizontalPosition = 255  - response[-4]
    #positionList.append((horizontalPosition, verticalPosition))
    #print(toc - tic)
    #print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
    #print(position)
    #plt.plot([position[0]],[position[1]],'ro')
    #plt.axis([0, 255, 0, 255])  
    #plt.show()
    #plt.clf()
    #print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
    
#fig = plt.figure()


#for position in positionList:
 #   plt.plot([position[0]],[position[1]],'ro')
  #  plt.axis([0, 255, 0, 255])  
   # plt.show()
    #plt.clf()
    
sensor.close()