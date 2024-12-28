from djitellopy import Tello
from ultralytics import YOLO
import cv2

# Connect to the Tello drone
tello = Tello()
tello.connect()

# Start the video stream
tello.streamon()

# Load the YOLO model
model = YOLO('9s.pt')  # Replace '9s.pt' with your trained model file

# Set up video capture
cap = tello.get_frame_read()

while True:
    # Get the current frame from the drone's camera
    frame = cap.frame

    # Resize the frame to a fixed size for better performance (optional)
    frame = cv2.resize(frame, (640, 480))

    # Convert frame to RGB (YOLO expects RGB format)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Perform inference
    results = model(frame_rgb)

    # Initialize object counter
    object_count = 0

    # Draw bounding boxes and count objects with confidence >= 50%
    for result in results[0].boxes:
        # Get bounding box coordinates
        x1, y1, x2, y2 = map(int, result.xyxy[0])  # Convert to integer
        conf = result.conf[0]  # Confidence score
        cls = int(result.cls[0])  # Class ID

        # Filter by confidence threshold
        if conf >= 0.50:  # 50% confidence threshold
            object_count += 1

            # Draw bounding box
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Green box

            # Add label text
            label = f'{cls} {conf:.2f}'
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Add the object count to the top-right corner of the frame
    text = f'Count: {object_count}'
    text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)[0]
    text_x = frame.shape[1] - text_size[0] - 10  # Right-aligned
    text_y = 30  # Top margin
    cv2.putText(frame, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)  # Blue text

    # Show the frame in a window
    cv2.imshow('Tello Drone Live Inference', frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Stop the video stream and release resources
tello.streamoff()
cv2.destroyAllWindows()
