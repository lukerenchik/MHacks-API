# -*- coding: utf-8 -*-
"""
Created on Tue Jan 10 13:09:37 2023

@author: Derek Joslin

"""

from PyQt5.QtWidgets import QLabel

class PeripheralDevice:
    def __init__(self, name):
        self.name = name
        self.debugString = ""
    
    def connect(self):
        pass
    
    def disconnect(self):
        pass
    
    def getStatus(self):
        return self.debugString

class PeripheralManager:
    def __init__(self):
        self.peripheralDictionary = {}
        
    def addPeripheral(self, Peripheral):
        self.peripheralDictionary[Peripheral.name] = Peripheral
        
    def removePeripheral(self, peripheralName):
        del self.peripheralDictionary[peripheralName]
        
    def getDevice(self, peripheralName):
        return self.peripheralDictionary.get(peripheralName)
        
    def getAllDevices(self):
        return self.peripheralDictionary.values()
    
    def connectAll(self):
        for peripheral in self.peripheralDictionary.values():
            peripheral.connect()
            
    def disconnectAll(self):
        for peripheral in self.peripheralDictionary.values():
            peripheral.disconnect()
            
    def getStatusAll(self):
        statuses = {}
        for peripheral in self.peripheralDictionary.values():
            statuses[peripheral.name] = peripheral.getStatus()
        return statuses
    
    def printAllPeripherals(self):
        peripheralDebugText = "ARCS Peripherals-\n"
        for Peripheral in self.peripheralDictionary.values():
            peripheralDebugText += "{}\n".format(Peripheral.name)
            peripheralDebugText += "{}\n".format(Peripheral.debugString)

        return peripheralDebugText
    
    def getPeripheralLabels(self):
        # create a list of labels for the peripherals
        peripheralLabelList = []

        for Peripheral in self.peripheralDictionary.values():
            # for each peripheral make a label
            Label = QLabel(Peripheral.name)
            
            # set the tooltip for this label to be the debug text of the peripheral
            Label.setToolTip(Peripheral.debugString)
            
            # add the perihperal label to the list
            peripheralLabelList.append(Label)

        return peripheralLabelList
# =============================================================================
# if __name__ == '__main__':
#     
#     peripheral_manager = PeripheralManager()
# 
#     peripheral1 = Peripheralperipheral("peripheral1", "Model1", "Vendor1")
#     peripheral2 = PeripheralDevice("peripheral2", "Model2", "Vendor2")
#     
#     peripheral_manager.add_device(device1)
#     peripheral_manager.add_device(device2)
#     
#     print(peripheral_manager.get_all_devices())
#     # Output: [<__main__.PeripheralDevice object at 0x7f1c1d4e7dd8>, <__main__.PeripheralDevice object at 0x7f1c1d4e7e48>]
#     
#     peripheral_manager.remove_device("Device1")
#     print(peripheral_manager.get_all_devices())
#     # Output: [<__main__.PeripheralDevice object at 0x7f1c1d4e7e48>]
# =============================================================================
