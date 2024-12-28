from ultralytics import YOLO
import cv2

# Load the model
model = YOLO('9s.pt')

# Read the image
img = cv2.imread('image.png')

# Run the model on the image
results = model(img)

# Convert image to RGB (YOLO expects RGB format)
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# Initialize a counter for detected objects
object_count = 0

# Draw bounding boxes with confidence >= 90%
for result in results[0].boxes:
    # Get bounding box coordinates
    x1, y1, x2, y2 = map(int, result.xyxy[0])  # Convert to integer
    conf = result.conf[0]  # Confidence score
    cls = int(result.cls[0])  # Class ID

    # Filter by confidence
    if conf >= 0.4:  # 50% confidence threshold
        # Increment the object count
        object_count += 1

        # Draw the bounding box
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Green box

        # Add label text
        label = f'{cls} {conf:.2f}'
        cv2.putText(img, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

# Convert back to BGR for OpenCV display
img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

# Add the count to the top-right corner
text = f'Count: {object_count}'
text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)[0]
text_x = img.shape[1] - text_size[0] - 10  # Right-aligned
text_y = 30  # Top margin
cv2.putText(img, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)  # Blue text

# Show the image in a window
cv2.imshow('Detections', img)

# Wait for a key press and close the window
cv2.waitKey(0)
cv2.destroyAllWindows()
