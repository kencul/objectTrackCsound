import cv2
from ultralytics import YOLO
import time

# Load the model
yolo = YOLO('yolo11n.pt')

# Load the video capture
results = yolo.track("https://www.youtube.com/watch?v=BxK9bwNfpoY", stream=True, stream_buffer = True, save = True, device= 'cuda:0', vid_stride=10)

# Function to get class colors
def getColours(cls_num):
    base_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
    color_index = cls_num % len(base_colors)
    increments = [(1, -2, 1), (-2, 1, -1), (1, -1, 2)]
    color = [base_colors[color_index][i] + increments[color_index][i] * 
    (cls_num // len(base_colors)) % 256 for i in range(3)]
    return tuple(color)

#-----------------------------
# Calculate the maximum scale for the frame
def findScale(result):
    height, width = result.orig_shape
    aspect_ratio = width / height

    screen_width, screen_height = 1728, 972  # Example screen resolution
    
    if height <= screen_height and width <= screen_width:
        print("Frame fits within screen dimensions.")
        return width, height

    print(f"Frame aspect ratio: {aspect_ratio}")
    max_scale_for_width = screen_width / (width)
    max_scale_for_height = screen_height / height

    # Calculate the maximum allowable scale to fit within screen dimensions
    if max_scale_for_width > 0 and max_scale_for_height > 0:
        max_scale = min(max_scale_for_width, max_scale_for_height)
    elif max_scale_for_width == 0 or max_scale_for_height == 0:
        max_scale = 1.0

    # Use the calculated scale to resize image
    new_width = int(width * max_scale)
    new_height = int(height * max_scale)
    print(f"Resized dimensions: {new_width}x{new_height}")
    return new_width, new_height

#-----------------------------
# Iterate over results and visualize detections
firstFrame = True
height, width = 0, 0
for result in results:
    if result is None:
        continue
    
    if firstFrame:
        firstFrame = False
        width, height = findScale(result)
    frame = result.plot()
    frame = cv2.resize(frame, (width, height))  # Resize frame for better display
    cv2.imshow('frame', frame)

    # Break the loop if 'q' is pressed
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

# release the video capture and destroy all windows
videoCap.release()
cv2.destroyAllWindows()

