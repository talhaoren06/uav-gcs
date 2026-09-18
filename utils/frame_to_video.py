import os
import cv2
import tkinter as tk
from tkinter import filedialog

# ---------------------------------------------------------
# 1. INITIALIZE GUI & FOLDER SELECTION
# ---------------------------------------------------------
# Create a root window and hide it (prevents empty window from showing)
root = tk.Tk()
root.withdraw()

# Open dialog for the user to select the directory containing frames
video_path = filedialog.askdirectory(title="Select video directory (Frames)")

# Safety check: Exit gracefully if the user cancels the folder selection
if not video_path:
    print("No directory selected. Exiting...")
    exit()

# ---------------------------------------------------------
# 2. FILTER & SORT IMAGE FILES
# ---------------------------------------------------------
clear_list = []
img_list = os.listdir(video_path)

# Collect only .jpg or .png files to prevent reading system files like .DS_Store
for img in img_list:
    if img.lower().endswith(".jpg") or img.lower().endswith(".png"):
        clear_list.append(img)

# Safety check: Exit if the selected folder has no images
if not clear_list:
    print("No images found in the selected directory. Exiting...")
    exit()

# Sort the frames sequentially to ensure smooth video playback
clear_list.sort()

# ---------------------------------------------------------
# 3. GET VIDEO RESOLUTION FROM THE FIRST FRAME
# ---------------------------------------------------------
first_img_path = os.path.join(video_path, clear_list[0])
first_img = cv2.imread(first_img_path)

# Extract height, width, and channels
h, w, c = first_img.shape

# ---------------------------------------------------------
# 4. PREPARE OUTPUT DIRECTORY & FILENAME
# ---------------------------------------------------------
current_path = os.path.dirname(os.path.abspath(__file__))
new_video_dir = os.path.join(current_path, "..", "Videos")

# Automatically create the 'Videos' folder if it doesn't exist
os.makedirs(new_video_dir, exist_ok=True)

# Get the desired video name from the terminal
video_name = input("Enter video name: ")

# Automatically append .mp4 extension if the user forgot it
if not video_name.lower().endswith(".mp4"):
    video_name += ".mp4"

new_video_path = os.path.join(new_video_dir, video_name)
print(f"The video will be saved here: {new_video_path}")

# ---------------------------------------------------------
# 5. COMPILE VIDEO
# ---------------------------------------------------------
# Initialize the OpenCV VideoWriter (30 FPS, mp4v codec)
videowriter = cv2.VideoWriter(new_video_path, cv2.VideoWriter_fourcc(*'mp4v'), 30, (w, h))

print("Compiling video... Please wait.")

# Loop through the sorted images and write them into the video file
for img in clear_list:
    img_path = os.path.join(video_path, img)
    frame = cv2.imread(img_path)
    videowriter.write(frame)

# Release the VideoWriter memory to finalize the .mp4 file
videowriter.release()
cv2.destroyAllWindows()

print("Video successfully created!")

