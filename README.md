# OVERWATCH TACTICAL GCS 🦅

A professional, multi-threaded Ground Control Station (GCS) software designed for Unmanned Aerial Vehicles (UAVs). Built with Python, PyQt5, and YOLOv8, this system provides real-time object detection, hardware telemetry monitoring, and automated tactical reporting.

## 🚀 Key Features

- **Real-Time Object Detection:** Integrated with Ultralytics YOLOv8 for high-FPS inference on live video feeds or pre-recorded MP4 files.
- **Dynamic Vision Settings:** Toggle bounding box labels, confidence scores, and filter specific target classes (e.g., Pedestrian, Car, Truck) on the fly without interrupting the feed.
- **Automated SITREP Terminal:** Generates and logs Situation Reports (SITREP) every 2 seconds, summarizing the detected targets on radar with timestamps.
- **Hardware Telemetry:** Live monitoring of System CPU and RAM usage via dynamic progress bars to prevent system overload during heavy OpenCV/PyTorch tasks.
- **Multi-Threaded Architecture:** Utilizes PyQt5 `QThread` to isolate the GUI from the heavy YOLO inference loop, ensuring a zero-lag, responsive interface.
- **Frame-to-Video Utility:** Includes a standalone `frame_to_video.py` script to compile dataset frames (.jpg/.png) into 30 FPS MP4 video feeds.

## 🛠️ Technology Stack

- **Language:** Python 3
- **GUI Framework:** PyQt5
- **Computer Vision:** OpenCV (`cv2`)
- **Deep Learning:** Ultralytics (YOLOv8)
- **Model Training** Jupyter Notebook, VisDrone Dataset
- **System Monitoring:** `psutil`

## ⚙️ Installation & Setup

1. **Clone the repository:**
```bash
git clone [https://github.com/talhaoren06/uav-gcs.git](https://github.com/talhaoren06/uav-gcs.git)
cd uav-gcs
```

2. **Create a virtual environment (Recommended):**
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Prepare the YOLO model:**
Create a folder named `models` in the root directory and place your trained YOLO weights (e.g., `best.pt`, `yolov8n.pt`) inside it.

## 🖥️ Usage

Run the main application interface:
```bash
python main.py
```
* **Connect Feed:** Starts the vision thread and detection algorithms.
* **Select Source:** Allows testing with different `.mp4` footage.
* **Disconnect:** Safely stops the worker thread and clears the feed.

Model Training (yolov8_visdrone_training.ipynb):
* Open the notebook using Jupyter Lab or Google Colab to review the dataset preparation, hyperparameter configuration, and training metrics for the YOLOv8 model.

## 👨‍💻 Author

**Ahmet Talha Ören**  
*Computer Engineering | Düzce Üniversitesi*

## 📝 License

This project is for educational and portfolio purposes.