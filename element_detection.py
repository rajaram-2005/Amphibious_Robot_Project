import cv2
import numpy as np
from tensorflow.keras.models import load_model

# Load the pre-trained CNN model for element classification
model = load_model('element_classification_model.h5')

# Labels for elements (this is a simplified list for the demo; replace with 118 element labels)
element_labels = ["Hydrogen", "Helium", "Lithium", "Beryllium", "Boron", "Carbon", ...]

# Function to preprocess the captured image for the model
def preprocess_image(img):
    img = cv2.resize(img, (224, 224))  # Resize to match the model input size
    img = img.astype("float") / 255.0  # Normalize the image
    img = np.expand_dims(img, axis=0)  # Add batch dimension
    return img

# Function to predict the element based on the image
def predict_element(img):
    processed_img = preprocess_image(img)
    predictions = model.predict(processed_img)
    element_id = np.argmax(predictions)  # Get the predicted element ID
    confidence = predictions[0][element_id]  # Confidence of the prediction
    return element_labels[element_id], confidence

# Initialize webcam or any connected camera
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()  # Capture frame-by-frame
    if not ret:
        break

    # Show the captured frame
    cv2.imshow('Element Detection', frame)

    # Check for 'q' key press to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Predict the element from the current frame
    element, confidence = predict_element(frame)
    print(f"Detected Element: {element} with confidence {confidence:.2f}")

# Release the camera and close windows
cap.release()
cv2.destroyAllWindows()
