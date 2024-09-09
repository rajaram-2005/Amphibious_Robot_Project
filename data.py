import time

def log_event(message):
    with open("Data/logs/robot_log.txt", "a") as log_file:
        timestamp = time.strftime("[%Y-%m-%d %H:%M:%S] ")
        log_file.write(timestamp + message + "\n")

# Example of logging sensor data and actions
sensor_data = "Water Sensor: 550, Soil Moisture: 420"
log_event(sensor_data)

log_event("Action: Switching to water propulsion")
