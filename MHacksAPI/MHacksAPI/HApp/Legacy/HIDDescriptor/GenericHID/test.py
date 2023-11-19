#%%

import sys
import usb.core
import usb.util

device = usb.core.find(idVendor=0x03EB,idProduct=0x1141)

if device is None:
    sys.exit("Device with specified Vendor ID and Product ID is missing.")

device.set_configuration()

list_of_ports = ['B', 'C', 'D', 'E', 'F']
ReportData = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]

while(1):
    mode_flag = input("Enter 'D' to set the direction for a Port, 'W' to write to a Port or 0 to exit.\n")

    if mode_flag == 'D':
        port_name = input("Enter Port name (B, C, D, E or F).\n")
        if port_name in list_of_ports:
            hex_value = input("Enter hex value.\n")

            ReportData[0] = ord(mode_flag)
            ReportData[1] = ord(port_name)
            ReportData[2] = int(hex_value, 16)

            device.ctrl_transfer(0x21, 9, 0x200, 0x00, ReportData)
            print('Direction for Port ' + port_name + ' has been set.')
        else:
            print('Port does not exist.')
    elif mode_flag == 'W':
        port_name = input("Enter Port name (B, C, D, E or F).\n")
        if port_name in list_of_ports:
            hex_value = input("Enter hex value.\n")
            
            ReportData[0] = ord(mode_flag)
            ReportData[1] = ord(port_name)
            ReportData[2] = int(hex_value, 16)
            
            device.ctrl_transfer(0x21, 9, 0x200, 0x00, ReportData)
            print('Data has been recorded to Port ' + port_name + '.')
        else:
            print('Port does not exist.')
    elif mode_flag == '0':
        break
    else:
        print('Invalid input.')