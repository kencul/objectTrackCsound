# VideoCsound
## Ken Kobayashi - 8/20/25

## Description

VideoCsound is a performance system that bridges computer vision and algorithmic composition. It analyzes live video feeds or pre-recorded videos using the YOLOv11 object detection model, tracks the movement of detected objects, and uses this data to generate synchronized, generative music in real-time via the Csound audio engine.

## Features

- **Real-time Object Detection & Tracking:** Leverages the Ultralytics YOLOv11 model to detect and track up to 80 different object types from the COCO dataset.

- **Generative Audio Synthesis:** Triggers and manipulates Csound instruments based on object type, position, and movement.

- **Multiple Video Sources:** Supports YouTube URLs, local video files (.mp4, .mov, etc.), and live webcam feeds.

- **Project-Based Configuration:** Simple YAML-based configuration system for managing different performances and sound designs.

- **Flexible Sound Design:** Each detected object type can be mapped to one or multiple custom Csound instruments.

## Requirements

- Python 3.8+
- FFmpeg (for YouTube downloads)
- Csound 7 - donwload the beta from the (Csound GitHub develop branch)[https://github.com/csound/csound]
- Git (Optional, for cloning repository)

## Installation

1. Clone or download repository

```bash
git clone <your-repository-url>
cd VideoCsound
```

2. Create a Virtual Environment (Recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

3. Install Required Python Packages
```bash
pip install -r requirements.txt
```

## Project Setup

VideoCsound uses a project-based system. Each performance or experiment should have its own directory containing three essential configuration files.

1. Run the main script pointing to your new directory. This will generate the necessary template files and then exit.

```bash
python processMP4.py my_performance
```

2. You can now edit the generated files in the my_performance/ folder to configure your piece.

## Configuration Files

1. ```config.yaml```

This file defines the core parameters for the program.

2. ```objects.yaml```

This file maps the 80 COCO object classes to Csound instrument numbers. The program will randomly choose an instrument from the list provided for each object type.

3. ```csound.csd```

This is your Csound orchestra file. Define your instruments here. The program will send data to your instruments via p-fields and control channels.

## Usage

1. Configure your project: Edit the three files (config.yaml, objects.yaml, csound.csd) in your project directory.

2. Run the program: Execute the main script from the terminal, passing the project directory name as the argument.
```bash
python processMP4.py my_performance
```

3. Interact with the program:

    - A window will open showing the video feed with bounding boxes and labels around detected objects.

    - Audio will be generated in real-time based on the objects and their movements.

    - Press q or ESC to quit the program.

## Troubleshooting

- Low Frame Rate: This is often caused by high-resolution video sources. Pre-process videos to 640x640 resolution or use the OUTPUT_WIDTH and OUTPUT_HEIGHT settings in config.yaml to downscale the display.

- Audio Lag: This is a known issue with the real-time processing approach of the program. Further investigation is needed to find the source of this issue

- Model Doesn't Detect My Object: The pre-trained YOLOv11 model is best at detecting common objects like people, cars, and animals. For best results, use video sources featuring these. For specialized objects, you would need to train a custom model.

- Csound Instruments Not Triggering: Double-check your objects.yaml file. Ensure the object name is spelled correctly (see the constants.py file for the full list) and that the instrument number matches an instrument defined in your csound.csd file.

## Acknowledgments

- Ultralytics for the YOLOv11 model and library.

- The Csound community for the powerful audio synthesis environment.

- OpenCV for computer vision utilities.