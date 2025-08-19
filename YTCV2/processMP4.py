# Library imports
from collections import defaultdict # for expanding list
import cv2 # for image processing
import numpy as np
from ultralytics import YOLO # for inference model
# import time # for frame timing
# from datetime import timedelta
#from cap_from_youtube import cap_from_youtube # to capture video from YouTube
import sys # for command line arguments
import os # for file path handling
from pathlib import Path # for path handling
import random # for random number generation
import yaml # for accessing yaml file

from csound import csound # for audio processing

# My script imports
import constants
import accessYaml # for accessing yaml data
#from genYaml import genYaml # for generating yaml file
import projectDir # for project directory management
import downloadYT # for downloading YouTube videos

# Get the first argument from command line and second will be URL to the YT video
if len(sys.argv) >= 2:
    url = sys.argv[1]
else:
    print("Error: Missing required argument. Please provide a folder path.")
    print("Usage: python processYTCV2.py <folder_path>")
    sys.exit(1)
    
# Check directory
if projectDir.check_project_dir(sys.argv[1]):
    sys.exit(1)  # If the directory was incomplete, exit the program

directory = Path(sys.argv[1])

# Load the model
yolo = YOLO('yolo11n.pt')

# Load project config
config_yaml = directory / 'config.yaml'
with open(config_yaml, 'r') as f:
    config_data = yaml.safe_load(f)

#-----------------------------------------------------------------
# Load the video capture
source = config_data.get('SOURCE', None)

# Select the source of the video based on the config
if source == 'YT':
    url = config_data.get('YT_URL', None)
    if not url:
        print("Error: YT_URL not found in config.yaml. Please provide a valid YouTube URL.")
        exit(1)
    video_file = downloadYT.check_local_file(url, directory)
    cap = cv2.VideoCapture(str(video_file))
elif source == 'VIDEO':
    video_path = config_data.get('VIDEO_FILE', None)
    if video_path is None:
        print("Error: VIDEO_FILE not found in config.yaml. Please provide a valid video file path.")
        exit(1)
    video_file = directory / video_path
    cap = cv2.VideoCapture(str(video_file))
elif source == "WEBCAM":
    cap = cv2.VideoCapture(0) # Use the default webcam
else:
    print("Error: Invalid SOURCE value in config.yaml. Please set to 'YT', 'VIDEO', or 'WEBCAM'.")

# Set start time if specified
start_time = config_data.get('YT_START_TIME', 0)  # Default start time is 0 seconds
fps = cap.get(cv2.CAP_PROP_FPS)
if start_time > 0:
    cap.set(cv2.CAP_PROP_POS_MSEC, start_time * 1000)


original_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
original_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
#frametime = int(1 / fps * 1000)

#----------------------------------------------------
# Calculate maximum scale for the frame while maintaining aspect ratio
def findScale(original_width, original_height):
    aspect_ratio = original_width / original_height
    
    print(f"Frame resolution: {original_width}x{original_height}, Aspect Ratio: {aspect_ratio:.2f}")
    max_scale_for_width = screen_width / original_width
    max_scale_for_height = screen_height / original_height

    # Calculate the maximum allowable scale to fit within screen dimensions
    if max_scale_for_width > 0 and max_scale_for_height > 0:
        max_scale = min(max_scale_for_width, max_scale_for_height)
    elif max_scale_for_width == 0 or max_scale_for_height == 0:
        max_scale = 1.0

    # Use the calculated scale to resize image
    new_width = int(original_width * max_scale)
    new_height = int(original_height * max_scale)
    print(f"Resized dimensions: {new_width}x{new_height}")
    return new_width, new_height

# Determine if resizing is needed

cv2.namedWindow('frame', cv2.WINDOW_AUTOSIZE)
screen_width, screen_height = config_data.get('SCREEN_WIDTH', None), config_data.get('SCREEN_HEIGHT', None)  # Fetch screen resolutions
needResizing = screen_width is not None and screen_height is not None
if needResizing:
    width, height = findScale(original_width, original_height)
    
        
# Function to get class colors
def getColours(cls_num):
    base_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
    color_index = cls_num % len(base_colors)
    increments = [(1, -2, 1), (-2, 1, -1), (1, -1, 2)]
    color = [base_colors[color_index][i] + increments[color_index][i] * 
    (cls_num // len(base_colors)) % 256 for i in range(3)]
    return tuple(color)

# Converting x and y coordinates to 0-1 scale
def x_ratio(x):
    """Converts an X coordinate to a 0-1 ratio based on the image width."""
    return x / original_width
 
def y_ratio(y):
    """Converts a Y coordinate to a 0-1 ratio based on the image height."""
    return y / original_height

# Accessing Yaml file to get instrument numbers for objects
yaml = accessYaml.AccessYaml(directory)

# --------------------------------------------------------------------
# Store the track history
track_history = defaultdict(lambda: [])

# Initialize Csound
cs = csound(directory)
res = cs.initialize()
if cs == 1:
    print("Csound initialization failed.")
    sys.exit(1)
cs.start()
cs.set_control_channel("freq", 110)
#playing = False

active_ids = {}

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    result = yolo.track(frame, 
                        persist=True, 
                        verbose=False, 
                        conf=config_data.get('YOLO_CONF_THRESHOLD', 0.3),
                        iou=config_data.get('YOLO_IOU_THRESHOLD', 0.5),
                        max_det=config_data.get('MAX_DETECTIONS', 3))[0]
    
    # Get the boxes and track IDs
    # REF: https://docs.ultralytics.com/reference/engine/results/#ultralytics.engine.results.Boxes
    if result.boxes and result.boxes.is_track: 
        boxes = result.boxes.xywh.cpu()
        track_ids = result.boxes.id.int().cpu().tolist()
        class_ids = result.boxes.cls.int().cpu().tolist()

        # Visualize the result on the frame
        frame = result.plot()
        # extra code...
        # Iterate through the boxes and track IDs
        for box, track_id, class_id in zip(boxes, track_ids, class_ids):
            x, y, w, h = box
            track = track_history[track_id]
            track.append((x, y))
            
            # send x y ratios to Csound
            cs.set_control_channel(f"x{track_id}", x_ratio(x))
            cs.set_control_channel(f"y{track_id}", 1 - y_ratio(y))
            cs.set_control_channel(f"w{track_id}", w / original_width)
            cs.set_control_channel(f"h{track_id}", h / original_height)
            
            if len(track) > 30:  # retain 30 tracks for 30 frames
                track.pop(0)

            # Draw the tracking lines
            points = np.hstack(track).astype(np.int32).reshape((-1, 1, 2))
            cv2.polylines(frame, [points], isClosed=False, color=(50, 230, 230), thickness=5)
            
            # Check if track_id is already playing
            if track_id not in active_ids.keys():
                instrNum = random.choice(yaml.access_data(constants.CLASSES[class_id]))
                active_ids[track_id] = (instrNum)
                cs.event_string(f"i {instrNum}.{track_id} 0 -1 {track_id} {config_data.get('BASE_FREQ', 440)} {config_data.get('AMP', 0.5)/config_data.get('MAX_DETECTIONS', 5)} {x} {y} {w} {h}")
                
        ids_to_remove = set(active_ids.keys()) - set(track_ids)
        for track_id in ids_to_remove:
            # Remove the track from active_ids
            instrNum = active_ids.pop(track_id)
            cs.event_string(f"i -{instrNum}.{track_id} 0 0")
            #print(f"Stopping track ID: {track_id}")
            
            # Remove the entry from track_history if needed
            if track_id in track_history:
                del track_history[track_id]           
    # If no boxes are detected, stop all active voices
    else:
        if len(active_ids) != 0:
            track_ids = list(active_ids.keys())
            for track_id in track_ids:
                instrNum = active_ids.pop(track_id)
                cs.event_string(f"i -{instrNum}.{track_id} 0 0")
            track_history.clear()
        
        
    # Resize frame for better display
    if needResizing:
        frame = cv2.resize(frame, (width, height))  

    # Show the image
    cv2.imshow('frame', frame)

    # Break the loop if 'q' is pressed
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q') or chr(key) == '\x1b':  # Check for 'q' or ESC key
        break
    
    # # Break loop if the window is closed
    # if cv2.getWindowProperty('image',cv2.WND_PROP_VISIBLE) < 1:        
    #     break

# release the video capture and destroy all windows
cv2.destroyAllWindows()
# Close the Csound thread
cs.close_thread()

