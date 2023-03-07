from picamera.array import PiRGBArray
from picamera import PiCamera
from pyzbar.pyzbar import decode
import time
import keyboard

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 60
rawCapture = PiRGBArray(camera, size=(640, 480))

# allow the camera to warmup
time.sleep(0.1)
camera.start_preview()

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    frame = frame.array

    # decode the barcode
    for code in decode(frame):
        print(code.type)
        print(code.data.decode('utf-8'))
        time.sleep(1)

    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)

    if keyboard.is_pressed('q'):
        print("get out")
        break


# this thing below is history
"""
# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 60
rawCapture = PiRGBArray(camera, size=(640, 480))

# allow the camera to warmup
time.sleep(0.1)

# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

    # grab the raw NumPy array representing the image, then initialize the timestamp
    # and occupied/unoccupied text
    image = frame.array

    # show the frame
    cv2.imshow("Frame", image)
    key = cv2.waitKey(1) & 0xFF

    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)

    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break
"""


# PART 2 THING

from picamera.array import PiRGBArray
from picamera import PiCamera
from pyzbar.pyzbar import decode
import time
import cv2

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 60
rawCapture = PiRGBArray(camera, size=(640, 480))

# allow the camera to warmup
time.sleep(0.1)
camera.start_preview()

# create a window to display the barcode information
cv2.namedWindow("Barcode Info", cv2.WINDOW_NORMAL)

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    frame = frame.array

    # decode the barcode
    for code in decode(frame):
        barcode_type = code.type
        barcode_data = code.data.decode('utf-8')

        # display the barcode information in the window
        cv2.putText(frame, f"{barcode_type}: {barcode_data}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        cv2.imshow("Barcode Info", frame)
        cv2.waitKey(0)

    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)

    # press 'q' to quit the program
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# release the camera and close the window
camera.stop_preview()
cv2.destroyAllWindows()
