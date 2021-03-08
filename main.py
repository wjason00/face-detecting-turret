import cv2
import RPi.GPIO as GPIO
import asyncio
from adafruit_servokit import ServoKit
from store import turret, camera

turret_1 = turret((19, 16, 26, 20))
camera_1 = camera(0)

if __name__ == "__main__":
    try:
        asyncio.run(camera_1.start_video(turret_1))

    except KeyboardInterrupt:
        turret_1.cleanup()  
          
