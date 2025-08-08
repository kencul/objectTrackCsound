import cv2 as cv
import numpy as np

# YOLOv11 classes (80 classes from COCO dataset)
classes = [
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

def main():
    img = cv.imread('imgs/asawa.jpg')
    if img is None:
        raise ValueError("Error: Could not read image")
        
    # Load the model
    yolo = YOLO('yolov8s.pt')
    
    blob = cv.dnn.blobFromImage(img, 1/255.0, (640, 640), swapRB=True)
    model.setInput(blob)
    outputs = model.forward()
    
    # DEBUG: Print raw outputs
    print("Raw output shape:", outputs.shape)
    print("Output sample:", outputs[0, :5, :5])
    
    # Process outputs
    try:
        outputs = np.squeeze(outputs).T
        print("Processed output shape:", outputs.shape)
        
        conf_threshold = 0.5
        scores = np.max(outputs[:, 4:], axis=1)
        keep = scores > conf_threshold
        outputs = outputs[keep, :]
        print(f"Found {len(outputs)} detections")
        
        if len(outputs) > 0:
            class_ids = np.argmax(outputs[:, 4:], axis=1)
            boxes = outputs[:, :4]
            
            # Draw detections
            img_height, img_width = img.shape[:2]
            for box, class_id, score in zip(boxes, class_ids, scores[keep]):
                intBox = box.astype(np.int32)
                x1, y1, x2, y2 = intBox
                x1 = int(max(0, x1/640 * img_width))
                y1 = int(max(0, y1/640 * img_height))
                x2 = int(min(img_width, x2/640 * img_width))
                y2 = int(min(img_height, y2/640 * img_height))
                print(f"Drawing box at ({x1}, {y1}), ({x2}, {y2}) for {classes[class_id]}")
                
                color = (0, 255, 0)
                cv.rectangle(img, (x1, y1), (x2, y2), color, 2)
                
                label = f"{classes[class_id]}: {score:.2f}"
                (tw, th), _ = cv.getTextSize(label, cv.FONT_HERSHEY_SIMPLEX, 0.6, 1)
                cv.rectangle(img, (x1, y1-th-10), (x1+tw, y1), color, -1)
                cv.putText(img, label, (x1, y1-5), cv.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,0), 1)
        else:
            print("No detections found!")
            
    except Exception as e:
        print(f"Processing error: {e}")

    cv.imshow("Detections", img)
    cv.waitKey(0)
    cv.destroyAllWindows()

if __name__ == "__main__":
    main()