import cv2
import ml_api
import pynput
import numpy as np

# cv2 opens a cam
# we take a pic by pressing some key
# that pic gets sent to the ml api to tell us what's it made of

# preferably without having to save and upload the pic, by for example using BytesIO (look it up on google)
