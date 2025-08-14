# Library imports
from collections import defaultdict # for expanding list
import cv2 # for image processing
import numpy as np
from ultralytics import YOLO # for inference model
import time # for frame timing
from datetime import timedelta
from cap_from_youtube import cap_from_youtube # to capture video from YouTube
import sys # for command line arguments
import os # for file path handling

from csound import csound # for audio processing
import constants

import random # for random number generation
import yaml # for accessing yaml file
import accessYaml # for accessing yaml data
from genYaml import genYaml # for generating yaml file
import projectDir # for project directory management

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

# Load the model
yolo = YOLO('yolo11n.pt')

# Load the video capture
# url = "https://www.youtube.com/watch?v=O0du5kMKHMk"   # Ireland
# url = "https://www.youtube.com/watch?v=alN1ePd2mrg" # cats
start_time = timedelta(seconds=constants.START_TIME)
cap = cap_from_youtube(url, '360p', start=start_time)

fps = cap.get(cv2.CAP_PROP_FPS)
original_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
original_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
frametime = int(1 / fps * 1000)

#-----------------------------
# Calculate the  scale for the frame
def findScale(original_width, original_height):
    aspect_ratio = original_width / original_height

    screen_width, screen_height = constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT  # Screen resolution to match

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
yaml = accessYaml.AccessYaml()

# --------------------------------------------------------------------
# Store the track history
track_history = defaultdict(lambda: [])

# Initialize Csound
cs = csound()
if cs == None:
    print("Csound initialization failed.")
    sys.exit(1)

cs.start()
cs.set_control_channel("freq", 110)
playing = False

active_ids = {}

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    result = yolo.track(frame, 
                        persist=True, 
                        verbose=False, 
                        conf=constants.YOLO_CONFIDENCE, 
                        iou=constants.YOLO_IOU_THRESHOLD,
                        max_det=constants.MAX_DETECTIONS)[0]
    
    # Get the boxes and track IDs
    # REF: https://docs.ultralytics.com/reference/engine/results/#ultralytics.engine.results.Boxes
    if result.boxes and result.boxes.is_track: 
        boxes = result.boxes.xywh.cpu()
        track_ids = result.boxes.id.int().cpu().tolist()
        class_ids = result.boxes.cls.int().cpu().tolist()

        # Visualize the result on the frame
        frame = result.plot()

        # Plot the tracks
        for box, track_id, class_id in zip(boxes, track_ids, class_ids):
            x, y, _, _ = box
            track = track_history[track_id]
            track.append((x, y))
            
            # send x y ratios to Csound
            cs.set_control_channel(f"x{track_id}", x_ratio(x))
            cs.set_control_channel(f"y{track_id}", 1 - y_ratio(y))
            # Debug
            # print(f"x ratio: {x_ratio(x)}, y ratio: {1 - y_ratio(y)}")
            # print(f"x coordinate: {x}, y coordinate: {y}")
            
            if len(track) > 30:  # retain 30 tracks for 30 frames
                track.pop(0)

            # Draw the tracking lines
            points = np.hstack(track).astype(np.int32).reshape((-1, 1, 2))
            cv2.polylines(frame, [points], isClosed=False, color=(50, 230, 230), thickness=5)
            
            # Check if track_id is already playing
            if track_id not in active_ids.keys():
                instrNum = random.choice(yaml.access_data(constants.CLASSES[class_id]))
                active_ids[track_id] = (instrNum)
                cs.event_string(f"i {instrNum}.{track_id} 0 -1 {track_id} {constants.BASE_FREQ} {constants.AMP/constants.MAX_DETECTIONS}")
            
            #print(f"Track ID: {track_id}, X: {x}, Y: {y}")
                
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
        if len(active_ids) == 0:
            continue  # No active tracks to stop
        
        track_ids = list(active_ids.keys())
        for track_id in track_ids:
            instrNum = active_ids.pop(track_id)
            cs.event_string(f"i -{instrNum}.{track_id} 0 0")
        track_history.clear()
        
        
    # Resize frame for better display
    # frame = cv2.resize(frame, (width, height))  

    # Show the image
    cv2.imshow('frame', frame)

    # Break the loop if 'q' is pressed
    key = cv2.waitKey(frametime) & 0xFF
    if key == ord('q'):
        break

# release the video capture and destroy all windows
cv2.destroyAllWindows()
# Close the Csound thread
cs.close_thread()

