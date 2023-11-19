# -*- coding: utf-8 -*-
"""
Created on Tue Oct 11 10:50:42 2022

@author: Derek Joslin
"""

import romReader as rr

filename = "C:\\Users\\derek\\OneDrive\\NewHaptics Shared\\HapticOS\\FC_GUI_API\\APIv0.7-Coeus\\v0.75-Coeus\\ROMs\\romTemplate.rom.py"

rom = open(filename)

thisCode = rom.read()
start = thisCode.find('@RomInputsBegin') + 15
end = thisCode.find('@RomInputsEnd')
dictionaryKeys = thisCode[start:end]
print(dictionaryKeys)

dictionaryKeys = dictionaryKeys.split()

#construct dictionary from values
newDictionary = {}

for key in dictionaryKeys:
    print(key)
    newDictionary[key] = 0



#thisRom = rr.romReader(filename)

#thisRom.executeRom()