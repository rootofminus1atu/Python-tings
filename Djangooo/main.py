import asyncio
from async_stuff.a1 import do_a1, do_a2
from barcode_improved_imporved import print_barcode_info

import cv2
from pyzbar.pyzbar import decode

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

while True:
    success, frame = cap.read()

    for code in decode(frame):
        print_barcode_info(code.data.decode('utf-8'))
        cv2.waitKey(1000)

    cv2.imshow('Testing-code-scan', frame)
    cv2.waitKey(1)











"""
async def main():
    task1 = asyncio.create_task(do_a1())
    task2 = asyncio.create_task(do_a2())
    await asyncio.gather(task1, task2)

# Call the main coroutine
asyncio.run(main())
"""
