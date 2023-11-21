# -*- coding: utf-8 -*-
"""
Created on Tue Jan 17 09:35:41 2023

@author: Derek Joslin

"""

0x05, 0x01, // Usage Page (Generic Desktop)
0x09, 0x02, // Usage (Mouse)
0xA1, 0x01, // Collection (Application)
0x09, 0x01, // Usage (Pointer)
0xA1, 0x00, // Collection (Physical)
0x05, 0x09, // Usage Page (Button)
0x19, 0x01, // Usage Minimum (Button 1)
0x29, 0x08, // Usage Maximum (Button 8)
0x15, 0x00, // Logical Minimum (0)
0x25, 0x01, // Logical Maximum (1)
0x95, 0x08, // Report Count (8)
0x75, 0x01, // Report Size (1)
0x81, 0x02, // Input (Data, Variable, Absolute)
0x95, 0x01, // Report Count (1)
0x75, 0x08, // Report Size (8)
0x81, 0x03, // Input (Constant)
0x05, 0x01, // Usage Page (Generic Desktop)
0x09, 0x30, // Usage (X)
0x09, 0x31, // Usage (Y)
0x09, 0x38, // Usage (Wheel)
0x15, 0x81, // Logical Minimum (-127)
0x25, 0x7F, // Logical Maximum (127)
0x75, 0x08, // Report Size (8)
0x95, 0x03, // Report Count (3)
0x81, 0x06, // Input (Data, Variable, Relative)
0xC0,       // End Collection
0xC0        // End Collection


// This report descriptor describes a device with 8 buttons, 3 relative axes (X, Y, and Wheel),
// and sends the data in 8-bit format. The usage of the buttons and the axes are described by the Usage Page and Usage fields.
// The Logical Minimum and Logical Maximum fields specify the range of values that can be sent for each field.
// The Report Count and Report Size fields specify how many fields of that size are present in the report,
// and the Input field specifies whether the field is data, constant, or relative.


// This is just an example of how the report descriptor can look like,
// it's not necessarily the best way to implement it for a Braille Display, depending on the device's characteristics
// and requirements the descriptor can vary. The actual implementation of the report descriptor
// would need to be tailored to the specific requirements of the Braille Display device.


#include <Windows.h>

#define MAX_BUTTONS 8
#define MAX_AXES 3

typedef struct {
    BYTE buttons[MAX_BUTTONS];
    BYTE axes[MAX_AXES];
} BRAILLE_REPORT;

HANDLE hDevice;

BOOL InitBrailleDevice() {
    // Open a handle to the device
    
    hDevice = CreateFile("\\\\.\\BrailleDisplay", GENERIC_READ | GENERIC_WRITE, 0, NULL, OPEN_EXISTING, 0, NULL);
    if (hDevice == INVALID_HANDLE_VALUE) {
        return FALSE;
    }

    // Set the device to use the report descriptor
    
    HIDP_CAPS caps;
    HidD_GetPreparsedData(hDevice, &preparsedData);
    HidP_GetCaps(preparsedData, &caps);
    if (caps.UsagePage != 0x01 || caps.Usage != 0x02) {
        CloseHandle(hDevice);
        return FALSE;
    }

    return TRUE;
}

BOOL ReadBrailleReport(BRAILLE_REPORT *report) {
    // Read the report from the device
    
    DWORD bytesRead;
    return ReadFile(hDevice, report, sizeof(BRAILLE_REPORT), &bytesRead, NULL);
}

BOOL WriteBrailleReport(BRAILLE_REPORT *report) {
    // Write the report to the device

    DWORD bytesWritten;
    return WriteFile(hDevice, report, sizeof(BRAILLE_REPORT), &bytesWritten, NULL);
}


// This is a simple example of how the HID Class Driver could be implemented in C for windows, 
// it shows how to open a handle to the device, how to read and write the reports, 
// and how to check that the device is using the correct report descriptor.


// It is important to note that this is a general example, 
// and it does not take into account all the necessary steps for a successful implementation, 
// such as error handling and validation of the input/output report. Also, it is not the only way to implement it, 
// and the implementation may vary depending on the operating system, the device and the requirements.


0x05, 0x0D, // Usage Page (Digitizer)
0x09, 0x05, // Usage (Touchscreen)
0x16, 0x00, 0x00, // Logical Minimum (0)
0x26, 0xFF, 0x7F, // Logical Maximum (32767)
0x75, 0x10,       // Report Size (16)
0x95, 0x03,       // Report Count (3)
0x81, 0x02,       // Input (Data, Variable, Absolute)


typedef struct {
    BYTE buttons[MAX_BUTTONS];
    BYTE axes[MAX_AXES];
    SHORT touchX;
    SHORT touchY;
    BYTE touchId;
    BYTE touchState;
} BRAILLE_REPORT;

BOOL ReadBrailleReport(BRAILLE_REPORT *report) {
    // Read the report from the device
    
    DWORD bytesRead;
    BOOL ret = ReadFile(hDevice, report, sizeof(BRAILLE_REPORT), &bytesRead, NULL);
    if (ret) {
        //Process touch screen data
        
        if (report->touchState) {
            printf("Touch at X:%d Y:%d with ID:%d\n", report->touchX, report->touchY, report->touchId);
        }
    }
    return ret;
}



