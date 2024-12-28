from djitellopy import Tello
from pynput import keyboard
import cv2
import threading
from ultralytics import YOLO

# Load the YOLO model
model = YOLO('9s.pt')

# Initialize Tello
tello = Tello()
tello.connect()

# Print the battery percentage
print(f"Battery: {tello.get_battery()}%")

# Function to display the drone's camera feed and run YOLO inference
def stream_camera_with_inference():
    tello.streamon()  # Turn on the camera stream
    while True:
        # Get the frame from the drone's camera
        frame = tello.get_frame_read().frame

        # Resize the frame (optional for better performance)
        frame = cv2.resize(frame, (640, 480))

        # Convert frame to RGB (YOLO expects RGB format)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Run YOLO model inference
        results = model(frame_rgb)

        # Initialize object counter
        object_count = 0

        # Draw bounding boxes and count objects with confidence >= 90%
        for result in results[0].boxes:
            # Get bounding box coordinates
            x1, y1, x2, y2 = map(int, result.xyxy[0])  # Convert to integer
            conf = result.conf[0]  # Confidence score
            cls = int(result.cls[0])  # Class ID

            # Filter by confidence threshold
            if conf >= 0.90:  # 90% confidence threshold
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

        # Display the frame
        cv2.imshow("Tello Camera Feed with YOLO Inference", frame)

        # Exit the video stream if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    tello.streamoff()
    cv2.destroyAllWindows()

# Define drone control functions
def ascend():
    tello.move_up(50)  # Move up by 50 cm

def descend():
    tello.move_down(50)  # Move down by 50 cm

def forward():
    tello.move_forward(50)  # Move forward by 50 cm

def back():
    tello.move_back(50)  # Move back by 50 cm

def move_left():
    tello.move_left(50)  # Move left by 50 cm

def move_right():
    tello.move_right(50)  # Move right by 50 cm

def spin_left():
    tello.rotate_counter_clockwise(45)  # Rotate counter-clockwise by 45 degrees

def spin_right():
    tello.rotate_clockwise(45)  # Rotate clockwise by 45 degrees

# Define key event handlers
def on_press(key):
    try:
        if key == keyboard.Key.up:  # Arrow up
            forward()
        elif key == keyboard.Key.down:  # Arrow down
            back()
        elif key == keyboard.Key.left:  # Arrow left
            move_left()
        elif key == keyboard.Key.right:  # Arrow right
            move_right()
        elif key.char == 'w':  # Key W
            ascend()
        elif key.char == 's':  # Key S
            descend()
        elif key.char == 'a':  # Key A
            spin_left()
        elif key.char == 'd':  # Key D
            spin_right()
    except AttributeError:
        pass  # Ignore special keys

def on_release(key):
    # Stop the drone on any key release (optional)
    if key == keyboard.Key.esc:  # Exit program on Esc key
        return False

# Main function
def main():
    # Start the camera streaming and inference in a separate thread
    camera_thread = threading.Thread(target=stream_camera_with_inference)
    camera_thread.daemon = True
    camera_thread.start()

    print("Tello control active. Use the following keys:")
    print("W: Ascend | S: Descend | A: Spin Left | D: Spin Right")
    print("Arrow Up: Forward | Arrow Down: Back | Arrow Left: Move Left | Arrow Right: Move Right")
    print("Press 'q' to stop the camera feed. Press 'Esc' to exit.")

    # Start the keyboard listener
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

# Run the program
if __name__ == "__main__":
    try:
        tello.takeoff()  # Take off the drone
        main()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        tello.land()  # Land the drone safely
        print("Drone landed.")
