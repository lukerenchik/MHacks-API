import serial


ser = serial.Serial('COM8', 115200, timeout=1)  # Adjust the timeout as needed
ser.write(bytearray([255]))


