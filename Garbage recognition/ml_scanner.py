import cv2
import requests
import os
import ml_api
import pynput
import numpy as np
from dotenv import load_dotenv
load_dotenv()

API_URL = "https://api-inference.huggingface.co/models/yangy50/garbage-classification"
headers = {"Authorization": f"Bearer {os.getenv('API_URL')}"}

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

while True:
    success, frame = cap.read()

    cv2.imshow('frame', frame)

    key = cv2.waitKey(1)
    if key == ord(' '):
        _, img_encoded = cv2.imencode('.jpg', frame)
        response = requests.post(API_URL, headers=headers, data=img_encoded.tobytes())

        if response.ok:
            predictions = response.json()
            print(predictions)
            cv2.waitKey(1000)
        else:
            print(f"Request failed with status code {response.status_code}")

    elif key == 27:  # 27 is the ASCII code for the Esc key
        break

cap.release()
cv2.destroyAllWindows()
