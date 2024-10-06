import cv2                              # cv2 to do Computer vision 
import numpy as np                      # all functions and math for the Mattresses
from keras.models import load_model     # to load modles from filse and work with them 

# Load the trained model
model       = load_model('flame_smoke_detection_model.h5')


# Function to preprocess the input frame
def preprocess_frame(frame):
    # Resize the frame to the input size of the model
    resized_frame = cv2.resize(frame, (400, 400))
    # Normalize pixel values to be between 0 and 1
    normalized_frame = resized_frame / 255.0
    # Expand dimensions to match the model's expected input shape
    input_frame = np.expand_dims(normalized_frame, axis=0)
    return input_frame

# Open a connection to the webcam (you may need to change the argument to 1 or 2 depending on your setup)
cap = cv2.VideoCapture(0)
# "http://192.168.0.103/stream"
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Perform detection on the frame
    input_frame = preprocess_frame(frame)
    prediction = model.predict(input_frame)

    # Display the frame with the detection result
    if prediction > 0.65:  # Assuming a threshold of 0.5 for binary classification
        cv2.putText(frame, f'Fire/Smoke Detected : {prediction}', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
    else:
        cv2.putText(frame, 'No Fire/Smoke Detected', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    cv2.imshow('Real-time Detection', frame)

    # Break the loop when 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all windows
cap.release()
cv2.destroyAllWindows()