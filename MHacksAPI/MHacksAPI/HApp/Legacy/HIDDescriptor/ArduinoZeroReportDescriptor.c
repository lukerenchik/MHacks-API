# -*- coding: utf-8 -*-
"""
Created on Tue Jan 17 15:35:15 2023

@author: Derek Joslin

"""

const uint8_t hidReportDescriptor[] = {
    // Usage Page (Generic Desktop)
    0x05, 0x01,
    // Usage (Braille Display)
    0x09, 0x06,
    // Collection (Application)
    0xA1, 0x01,
    // Usage (Solenoid Valve 1-15)
    0x09, 0x01,
    // Logical Minimum (0)
    0x15, 0x00,
    // Logical Maximum (1)
    0x25, 0x01,
    // Report Size (1)
    0x75, 0x01,
    // Report Count (15)
    0x95, 0x0F,
    // Input (Data, Variable, Absolute)
    0x81, 0x02,
    // Usage (Touchscreen)
    0x09, 0x05,
    // Collection (Physical)
    0xA1, 0x00,
    // Usage Page (Digitizer)
    0x05, 0x0D,
    // Usage (Touchscreen)
    0x09, 0x04,
    // Logical Minimum (0)
    0x15, 0x00,
    // Logical Maximum (32767)
    0x26, 0xFF, 0x7F,
    // Report Size (16)
    0x75, 0x10,
    // Report Count (2)
    0x95, 0x02,
    // Input (Data, Variable, Absolute)
    0x81, 0x02,
    // End Collection
    0xC0,
    // End Collection
    0xC0
};

# =============================================================================
# 
# The report descriptor is a binary data structure that describes the behavior of an HID device. It provides information about the device's data packets and how the host computer should interpret them. The report descriptor is used by the host computer to understand the device and communicate with it.
# 
# This example report descriptor describes a braille display with 15 solenoid valves as output and a touchscreen input. It starts by specifying the usage page and usage for the device, in this case, the usage page is Generic Desktop (0x01) and the usage is Braille Display (0x06). This information is defined by the USB-IF (USB Implementers Forum) in the HID Usage Tables specification (https://www.usb.org/document-library/hid-usage-tables-111).
# 
# Then, it defines a collection of items, in this case, an application collection (0xA1, 0x01), which contains the usage of the 15 solenoid valves as output. The report size (0x75, 0x01) and report count (0x95, 0x0F) specify that each solenoid valve is represented by 1-bit and there are 15 solenoids valves, respectively. The input type (0x81, 0x02) indicates that this is a data variable, the logical minimum (0x15, 0x00) and logical maximum (0x25, 0x01) represent that the solenoids valves can be either on (1) or off (0). This information is defined by the USB-IF in the HID 1.11 specification (https://www.usb.org/document-library/hid-111).
# 
# Lastly, it defines the touchscreen input, which is represented by the collection of items (0xA1, 0x00) and the usage page (0x05, 0x0D) and usage (0x09, 0x04) of the touchscreen. The report size (0x75, 0x10) and report count (0x95, 0x02) specify that the touchscreen input is represented by 2 sets of 16-bit, respectively. The logical minimum (0x15, 0x00), logical maximum (0x26, 0xFF, 0x7F) and input type (0x81, 0x02) indicate that the touchscreen input is a data variable and it's values can range from 0 to 32767, respectively.
# 
# It's important to note that report descriptor example is a rough one, and it's missing some important parts of the code and it's not tailored to the specific requirements or capabilities of any particular device. To implement a real-world device, you should consult the documentation of the specific USB controller and microcontroller you are using, as well as the USB standard that the device is using to understand the communication protocol and the format of the data being sent and also you should use the appropriate libraries and functions that are available.
# 
# 
# =============================================================================
