# constants.py

# YOLO model path and parameters
YOLO_MODEL_PATH = 'yolo11n.pt'
YOLO_CONFIDENCE = 0.3
YOLO_IOU_THRESHOLD = 0.5
MAX_DETECTIONS = 1   # Controls the max number of detections

# YouTube video settings
DEFAULT_YT_URL = "https://www.youtube.com/watch?v=O0du5kMKHMk"
START_TIME = 5000  # Start time for video capture

# Screen scaling
SCREEN_WIDTH = 1728
SCREEN_HEIGHT = 972

# Other constants
BASE_FREQ = 110  # Frequency for Csound audio
AMP = 0.5

# COCO object classes
CLASSES = [
    "person", "bicycle", "car", "motorcycle", "airplane", "bus", "train", "truck", "boat",
    "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
    "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack",
    "umbrella", "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball",
    "kite", "baseball bat", "baseball glove", "skateboard", "surfboard", "tennis racket",
    "bottle", "wine glass", "cup", "fork", "knife", "spoon", "bowl", "banana", "apple",
    "sandwich", "orange", "broccoli", "carrot", "hot dog", "pizza", "donut", "cake", "chair",
    "couch", "potted plant", "bed", "dining table", "toilet", "tv", "laptop", "mouse",
    "remote", "keyboard", "cell phone", "microwave", "oven", "toaster", "sink", "refrigerator",
    "book", "clock", "vase", "scissors", "teddy bear", "hair drier", "toothbrush"
]

YAML_PATH = 'output.yaml'