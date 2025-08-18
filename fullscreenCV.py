import cv2

# Replace 'your_image.jpg' with your image file path
image = cv2.imread('imgs/asawa.jpg')

if image is not None:
    cv2.namedWindow("Fullscreen Window", cv2.WINDOW_FULLSCREEN)
    cv2.imshow("Fullscreen Window", image)

    # Wait for a key press to exit
    while True:
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyWindow("Fullscreen Window")
else:
    print("Error: Image not loaded")