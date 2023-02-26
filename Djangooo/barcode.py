import cv2
from pyzbar.pyzbar import decode

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

while True:
    success, frame = cap.read()

    for code in decode(frame):
        #barcode_num = code.data.decode('utf-8')
        #barcode_type = code.type
        #if barcode_num then something to not make it rescan it many times over and over

        print(code.type)
        print(code.data.decode('utf-8'))

    cv2.imshow('Testing-code-scan', frame)
    cv2.waitKey(1)