# -*- coding: utf-8 -*-
"""
Created on Wed Oct 11 14:17:20 2023

@author: Derek Joslin

"""

SERIAL_INIT_ERROR = """{args} is an incorrect arguement.
      To create DisplaySerial parameters should be 
      comportString, baudrate, timeout
      default is "[yourComportString]", 115200, 3"""
      
      
SERIAL_NO_CONFIRMBYTE_RESPONSE_ERROR = """No confirmation byte recieved from the display,
known causes:
    Check that this is not old pro micro firmware which does not respond a confirm byte on connection
    Check that the hardware descriptor has the correct serialport if using pro micro
    Check hardware connection of tx and rx pins
    Check that the device is not in the process of resetting
    If connecting to the Nano it restarts and needs a delay before sending the confirmByte"""
    
SERIAL_INCORRECT_CONFIRMBYTE_RESPONSE_ERROR = """Unable to read confirmation bit of 255 from the display,
known causes:
    Incorrect baudrate
    Confirmation byte code changed"""

SERIAL_INCORRECT_NUMBER_OF_ROWS_ERROR = ""