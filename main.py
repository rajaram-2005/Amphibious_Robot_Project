import bluetooth_comm
import gps_control
import sensor_analysis
import element_detection
import time

# Main loop for controlling robot functions
def main():
    while True:
        # Get GPS location
        lat, lon = gps_control.get_gps_location()
        print(f"Current GPS Location: {lat}, {lon}")

        # Read sensor data from Arduino
        sensor_data = bluetooth_comm.read_from_arduino()
        print(f"Sensor Data: {sensor_data}")

        # Check for thunderstorm detection
        if "THUNDER_DETECTED" in sensor_data:
            print("Thunderstorm detected! Returning to base.")
            return_to_base()

        # Analyze sensor data
        decision = sensor_analysis.analyze_data(sensor_data)
        if "Element Detected" in sensor_data:
            element_id = int(sensor_data.split("Element Detected: ")[1])
            decision = element_detection.analyze_element_data(element_id)

        # Send commands based on analysis
        if decision == "STOP":
            bluetooth_comm.send_to_arduino('S')
        elif decision == "COLLECT_SAMPLE":
            bluetooth_comm.send_to_arduino('C')

        time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Program interrupted.")
