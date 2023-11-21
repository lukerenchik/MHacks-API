# -*- coding: utf-8 -*-
"""
Created on Thu Oct  6 10:08:09 2022

@author: Derek Joslin
"""

import threading

""" reads settings from rom file and starts executing rom in seperate thread """

class RomReader(threading.Thread):
    
    def __init__(self, filename):
                
        super().__init__()
        self.lock = threading.Lock()
        self.stopEvent = threading.Event()
        
        #open the rom
        self.rom = open(filename)
        self.romString = self.rom.read()
        
        
        thisCode = self.romString
        start = thisCode.find('@RomInputsBegin') + 17
        end = thisCode.find('@RomInputsEnd')
        
        inputCode = thisCode[start:end]
        
        settingList = inputCode.split('#')
        
        self.interruptDictionary = {}
        self.romSettings = {}
        self.commentList = []
        
        for settingLine in settingList:
            commentList = settingLine.split('\n')
            valuesList = commentList[1].split('=')
            self.commentList.append(commentList[0])
            valuesList[1] = valuesList[1].replace(" ", "")
            self.romSettings[valuesList[0].replace(" ", "")] = valuesList[1].replace('"', "")
# =============================================================================
#             
#         print(self.romSettings)
#         print(self.commentList)
# =============================================================================
        
    def createInterruptDictionary(self):
        romInterruptNames = self.getInterruptNames()
        
        for romInterruptString in romInterruptNames:
            self.interruptDictionary[romInterruptString] = 0#initial Value
            
        interruptDictionaryAddress = id(self.interruptDictionary)
            
        self.romSettings['interruptDictionaryAddress'] = interruptDictionaryAddress
        
        return self.interruptDictionary
            
    def getInterruptNames(self):
        interruptDictionaryAddress = self.romSettings['interruptDictionaryAddress']
        #get rid of id
        interruptDictionaryAddress = interruptDictionaryAddress[3:-1]
        
        interruptDictionaryAddress = interruptDictionaryAddress.replace('{', "")
        interrupts = interruptDictionaryAddress.split(',')
        interruptNames = []
        for interrupt in interrupts:
            interruptName = interrupt.split(':')
            interruptName = interruptName[0]
            interruptName = interruptName.replace("'","")
            interruptNames.append(interruptName)
            
        return interruptNames
        
    def setInterruptFlag(self, romInterruptString, value):
        self.interruptDictionary[romInterruptString] = value
        
    def getSettings(self):
        return self.romSettings
        
    def getDescriptions(self):
        return self.commentList
    
    def setSettings(self, settingDict):
        self.romSettings = settingDict
        
    def executeRom(self):
        self.start()
        return self.is_alive()
            
    def endRom(self):
        self.join()
        
    def run(self):
        self.romSettings['stopEvent'] = self.stopEvent
        with self.lock:
            # block simultanous execution of shared variables
            exec(self.romString,self.romSettings)
