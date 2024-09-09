import serial
import time

# Establish serial communication with Arduino
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
time.sleep(2)  # Wait for the connection to establish

# Send data to Arduino
def send_to_arduino(command):
    ser.write(command.encode())
    time.sleep(0.5)
    response = ser.readline().decode('utf-8').strip()
    print("Arduino Response: ", response)

# Read data from Arduino
def read_from_arduino():
    if ser.in_waiting > 0:
        data = ser.readline().decode('utf-8').strip()
        return data
    return None
