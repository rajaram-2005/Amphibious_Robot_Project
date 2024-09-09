# Analyze sensor data and make a decision
def analyze_data(sensor_data):
    if "Water" in sensor_data and int(sensor_data["Water"]) > 500:
        return "STOP"  # If water level is above threshold, stop the robot
    elif "Soil Moisture" in sensor_data and int(sensor_data["Soil Moisture"]) > 400:
        return "COLLECT_SAMPLE"  # If soil moisture is above threshold, collect sample
    else:
        return "CONTINUE"  # Continue normal operation
