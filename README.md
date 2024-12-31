# 🚁 AI Driven Crop Yeild Analysis using DJI Tello Drone 🤖

Check out my youtube vlog on the whole process: <link> 📺


## 🌟 Features

- Real-time object detection using YOLO model
- Multiple operation modes:
  - 📷 Static image processing
  - 🎥 Webcam live detection
  - 🛸 Tello drone camera stream
  - 🎮 Drone flight control with object detection

## 🛠️ Prerequisites

- Python 3.8+
- OpenCV (`cv2`)
- DJI Tello drone
- Required Python packages:
  ```
  djitellopy
  ultralytics
  opencv-python
  pynput
  ```

## 📁 Project Structure

- `inference.py` - Static image object detection
- `live_inference.py` - Webcam-based real-time detection
- `Tello_Combined.py` - Full drone control with object detection
- `tello_control.py` - Basic drone flight controls
- `tello_stream.py` - Drone camera stream with object detection

## 🎮 Controls

### Drone Movement Controls
- ⬆️ Forward: Arrow Up
- ⬇️ Backward: Arrow Down
- ⬅️ Left: Arrow Left
- ➡️ Right: Arrow Right
- 🔼 Ascend: W
- 🔽 Descend: S
- ↪️ Rotate Left: A
- ↩️ Rotate Right: D
- 🛑 Exit: ESC
- 📷 Stop Camera Feed: Q

## 🚀 Getting Started

1. Install required packages:
   ```bash
   pip install djitellopy ultralytics opencv-python pynput
   ```

2. Connect to your Tello drone's WiFi network

3. Choose your preferred operation mode:

   - For static image detection:
   ```bash
   python inference.py
   ```

   - For webcam detection:
   ```bash
   python live_inference.py
   ```

   - For full drone control with detection:
   ```bash
   python Tello_Combined.py
   ```

## 🎯 Detection Features

- Real-time object detection and counting
- Confidence threshold filtering (adjustable)
- Bounding box visualization
- Object count display
- Class ID and confidence score labels

## ⚙️ Configuration

- Default confidence thresholds:
  - Static image: 40%
  - Live webcam: 60%
  - Drone stream: 90%
- Drone movement distance: 50cm (adjustable in code)
- Rotation angle: 45 degrees

## 🔍 YOLO Model

The project uses a custom YOLO model (`9s.pt`). Make sure to:
- Place your model file in the project directory
- Update the model path in the code if using a different model

## ⚠️ Safety Notes

- Always operate the drone in a safe, open area
- Maintain visual line of sight with the drone
- Monitor battery levels regularly
- Follow local drone operation regulations
- Test object detection separately before combining with drone flight

## 🐛 Troubleshooting

- If the drone doesn't connect, check your WiFi connection
- Ensure the battery is sufficiently charged
- Verify all required packages are installed
- Check if the YOLO model file exists in the correct location
- Monitor console output for error messages

## 🔄 Future Improvements

- [ ] Add autonomous tracking capabilities
- [ ] Implement gesture-based controls
- [✅] Add data logging and analytics
- [✅] Improve detection performance
- [ ] Add multiple object class support
