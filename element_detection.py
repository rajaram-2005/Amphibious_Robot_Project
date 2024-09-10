import csv
import time
import os
import bluetooth_comm  # Custom module for communication with Arduino (robotic arm control)

# Path to save element data
data_file = "Data/new_element_data.csv"
image_folder = "Data/element_images/"

# Function to log new element data and trigger the robotic arm for sample collection
def log_new_element_and_collect_sample(element_id, temperature, pressure, ph_level, image_path):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    
    # Log the new element data in the CSV file
    with open(data_file, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, element_id, temperature, pressure, ph_level, image_path])
    
    # Trigger the robotic arm to collect the sample
    print(f"New element detected: {element_id}. Collecting sample using robotic arm.")
    bluetooth_comm.send_to_arduino('C')  # Command to collect sample (Arduino controls the robotic arm)
    
    # Log event
    log_event(f"New element detected: {element_id}, sample collected.")
    
    print(f"New element data logged and sample collected: {element_id}, Image: {image_path}")

# Function to log events
def log_event(message):
    timestamp = time.strftime("[%Y-%m-%d %H:%M:%S]")
    with open("Data/logs/robot_log.txt", "a") as log_file:
        log_file.write(f"{timestamp} {message}\n")

# Example usage when a new element is detected
element_id = 119  # Simulated new element ID
temperature = 25.4  # Example sensor data
pressure = 1013  # Example sensor data
ph_level = 7.2  # Example sensor data
image_path = os.path.join(image_folder, "element_119.jpg")

# Log the new element data and trigger robotic arm for sample collection
log_new_element_and_collect_sample(element_id, temperature, pressure, ph_level, image_path)
