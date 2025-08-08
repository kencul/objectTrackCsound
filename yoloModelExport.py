
from ultralytics import YOLO

def train_model():
    # Load a model
    model = YOLO("yolo11n.pt")  # or your custom model
    
    # Train the model
    results = model.train(
        data="coco128.yaml",
        epochs=10,
        imgsz=640
    )
    
    results = model.val()

    # Perform object detection on an image using the model
    results = model("https://ultralytics.com/images/bus.jpg")

    # Export the model to ONNX format
    model.save('myYolo11.pt')

if __name__ == '__main__':
    train_model()