import cv2

# create a VideoCapture object to capture images from the camera
cap = cv2.VideoCapture(0)

# check if the camera is opened correctly
if not cap.isOpened():
    print("Cannot open camera")
    exit()

# capture an image from the camera
ret, frame = cap.read()

# if the capture was successful, save the image
if ret:
    cv2.imwrite("captured_image.jpg", frame)

# release the VideoCapture object and close the window
cap.release()
cv2.destroyAllWindows()