# -*- coding: utf-8 -*-
"""
Created on Tue Feb 14 11:32:32 2023

@author: Derek Joslin

"""


import serial

ser = serial.Serial('COM7', 115200)  # Open serial port



# Send byte array
byte_array = bytearray([1, 2, 3, 0, 2, 4, 35, 0, 3, 2, 1])
ser.write(byte_array)

comportBytes = []  # Create empty list to store received bytes

while True:
    if ser.in_waiting > 0:  # Check if there are bytes in the input buffer
        byte = ser.read()  # Read a single byte from the serial port
        comportBytes.append(byte)  # Add the byte to the list
    
    i = 0
    if len(comportBytes) == 45:
        comportBytes[0:7] = []
        comportBytes[-3:-1] = []
        byteString = ""
        for byte in comportBytes:
            byteString += ' {} '.format(int.from_bytes(byte, byteorder='big', signed=False))
            i += 1
            if i > 5:
                byteString += "\n"
                i = 0
            
        print(byteString)
        print("\n" * 35)
# =============================================================================
#         my_bytes = bytearray(comportBytes)
#         try:
#             decoded_text = my_bytes.decode('utf-8')
#         except UnicodeDecodeError as e:
#             print('Error decoding bytes:', e)
#             decoded_text = 'Error: could not decode bytes'
#         print(decoded_text)
# =============================================================================
        comportBytes.clear()
        ser.write(byte_array)


ser.close()  # Close the serial port when done

# Print the received bytes as a string
#print('Received bytes:', bytearray(comportBytes).decode())
