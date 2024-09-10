import cv2
import os
import time
import serial
import re
import csv
from collections import Counter

# === SECTION 1: Image Comparison for Element Detection === #

# Path to the folder containing known element images
element_image_path = 'element_images/'

# Load images of known elements into a dictionary
known_elements = {}
for filename in os.listdir(element_image_path):
    if filename.endswith(".jpg"):
        element_name = filename.split('.')[0]
        element_image = cv2.imread(os.path.join(element_image_path, filename), cv2.IMREAD_GRAYSCALE)
        known_elements[element_name] = element_image

# Function to match captured image with known elements
def match_element(captured_image):
    captured_gray = cv2.cvtColor(captured_image, cv2.COLOR_BGR2GRAY)
    for element_name, element_image in known_elements.items():
        # Resize the known element image to match the captured image size
        element_resized = cv2.resize(element_image, (captured_gray.shape[1], captured_gray.shape[0]))

        # Compare the captured image to the known element images
        difference = cv2.absdiff(captured_gray, element_resized)
        _, difference = cv2.threshold(difference, 50, 255, cv2.THRESH_BINARY)
        non_zero_count = cv2.countNonZero(difference)

        # If images are similar (low difference), return the element
        if non_zero_count < 1000:  # Threshold for considering a match
            return element_name

    return "Unknown Element"  # Return unknown if no match is found


# === SECTION 2: Communication with Arduino === #

# Establish serial communication with Arduino
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
time.sleep(2)

def send_to_arduino(command):
    ser.write(command.encode())
    time.sleep(0.5)
    response = ser.readline().decode('utf-8').strip()
    print(f"Arduino Response: {response}")


# === SECTION 3: Logging Events === #

# Function to log events to a file
def log_event(message):
    timestamp = time.strftime("[%Y-%m-%d %H:%M:%S]")
    with open("Data/logs/robot_log.txt", "a") as log_file:
        log_file.write(f"{timestamp} {message}\n")


# === SECTION 4: Main Function with Real-Time Data Analysis === #

# Main function to control the robot's operation and perform data analysis
def main():
    # Initialize OpenCV camera capture
    cap = cv2.VideoCapture(0)

    # Initialize a dictionary to store new element detection counts
    new_elements_detected = {}

    try:
        while True:
            # Capture frame from camera
            ret, frame = cap.read()
            if not ret:
                print("Error: Unable to capture image from camera.")
                break

            # Display the captured frame
            cv2.imshow('Element Detection', frame)

            # Match the captured image with known elements
            element_name = match_element(frame)
            print(f"Detected Element: {element_name}")

            # If unknown element is detected, trigger sample collection and log
            if element_name == "Unknown Element":
                print("Unknown element detected. Collecting sample...")
                send_to_arduino('C')  # Command to collect sample
                log_event("New element detected, sample collected.")

                # Update real-time analysis for new elements
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                if timestamp in new_elements_detected:
                    new_elements_detected[timestamp] += 1
                else:
                    new_elements_detected[timestamp] = 1

            else:
                print(f"Known element: {element_name}. Continuing operation...")
                log_event(f"Detected known element: {element_name}")

            # Check for 'q' key press to exit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("Exiting...")
                break

            time.sleep(1)  # Delay for smooth execution

    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        # Release the camera and close OpenCV windows
        cap.release()
        cv2.destroyAllWindows()

        # After detection is done, write new element analysis to CSV
        write_analysis_to_csv(new_elements_detected)


# === SECTION 5: Writing Real-Time Analysis to CSV === #

# Function to write analysis of new elements to CSV file
def write_analysis_to_csv(new_elements_detected):
    output_csv_path = "Data/logs/element_analysis.csv"
    
    with open(output_csv_path, "w", newline="") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["Timestamp", "Number of New Element Detections"])
        for timestamp, count in new_elements_detected.items():
            csv_writer.writerow([timestamp, count])

    print(f"Analysis complete. Results saved to {output_csv_path}")


# === SECTION 6: Execute the Main Program === #

if __name__ == "__main__":
    # Run the main function for element detection and real-time analysis
    main()
