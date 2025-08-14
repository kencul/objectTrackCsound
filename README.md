## References

- [Getting started with YOLO in opencv for Object Detection](https://www.geeksforgeeks.org/computer-vision/object-detection-with-yolo-and-opencv/)

This website was a good introduction for code for object detection from the webcam. The example code at the end works straight out of the box, and was a basis for my code

- [Quick start YOLO with ultralytics](https://docs.ultralytics.com/quickstart/#conda-docker-image)

Getting Ultralytics set up was important to delve into inference models. They provide the YOLO model, which is what I am using for object detection and tracking. It also introduced me to PyTorch and Cuda for training my own models. Although not needed for this project, models can be trained for a specific application, instead of the generic everyday objects that the pretrained models detect. However, this project will do just fine with the pretrained models.

- [Model Prediction with Ultralytics YOLO](https://docs.ultralytics.com/modes/predict/)

Documentation on inference using YOLO in Ultralytics. Although tracking (which keeps track of each object and their movements) is more applicable for this project, this page has specific documentation on arguments, attributes, and methods of many of the methods I am using. It also has example code snippets and general precautions useful for using YOLO in ultralytics.

- [Object Tracking with Ultralytics YOLO](https://docs.ultralytics.com/modes/track/)

Documentation on object tracking using YOLO in Ultralytics. Main function of YOLO used in this project. Has example code of how to set up object tracking and examples in Python.

- [Python Library for Grabbing Youtube videos to process with CV](https://github.com/ibaiGorordo/cap_from_youtube/tree/main)

Using this library is gives more control than Ultralytic functions' youtube grabber. Using this library fixed stuttering due to buffering/fps issues by lowering the quality of the input video.

- [Code example for drawing tracking lines with CV2 and Ultralytics YOLO](https://docs.ultralytics.com/modes/track/#plotting-tracks-over-time)

This code snippet was used to visualize the movement of the detected objects.

- [YT-DLP](https://github.com/yt-dlp/yt-dlp)

What cap_from_youtube is built on. Better for downloading and access to metadata