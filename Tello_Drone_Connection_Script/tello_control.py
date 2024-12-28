from djitellopy import Tello
from pynput import keyboard

# Initialize Tello
tello = Tello()
tello.connect()

DISTANCE = 10
ANGLE = 30

# Print battery level (optional)
print(f"Battery: {tello.get_battery()}%")

# Define drone control functions
def ascend():
    tello.move_up(DISTANCE)  # Move up by DISTANCE cm

def descend():
    tello.move_down(DISTANCE)  # Move down by DISTANCE cm

def forward():
    tello.move_forward(DISTANCE)  # Move forward by DISTANCE cm

def back():
    tello.move_back(DISTANCE)  # Move back by DISTANCE cm

def move_left():
    tello.move_left(DISTANCE)  # Move left by DISTANCE cm

def move_right():
    tello.move_right(DISTANCE)  # Move right by DISTANCE cm

def spin_left():
    tello.rotate_counter_clockwise(ANGLE)  # Rotate counter-clockwise by 45 degrees

def spin_right():
    tello.rotate_clockwise(ANGLE)  # Rotate clockwise by 45 degrees

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

# Main logic
def main():
    print("Starting Tello control. Use the mapped keys to control the drone:")
    print("W: Ascend | S: Descend | A: Spin Left | D: Spin Right")
    print("Arrow Up: Forward | Arrow Down: Back | Arrow Left: Move Left | Arrow Right: Move Right")
    print("Press Esc to exit.")

    # Start the keyboard listener
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

# Run the main function
if __name__ == "__main__":
    try:
        tello.takeoff()
        main()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        tello.land()
        print("Drone landed.")
