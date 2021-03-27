import cv2
import RPi.GPIO as GPIO
from time import sleep
from math import floor
from adafruit_servokit import ServoKit
from constants import DIR, STEP, CW, CCW, SPR, DELAY, MS_PINS, RESOLUTION, RESOLUTION_CHOICE

# Creating a class for controlling the turret
class turret():
    def __init__(self):
        # Settings for controlling the DRV8825 & NEMA17
        GPIO.setwarnings(False) 
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(DIR, GPIO.OUT)
        GPIO.setup(STEP, GPIO.OUT)
        GPIO.output(DIR, CW) # Setting the direction equal to the wanted direction (1, 0)

        # Setting up microstepping
        GPIO.setup(MS_PINS, GPIO.OUT)
        GPIO.output(MS_PINS, RESOLUTION[RESOLUTION_CHOICE])

        # Setting up the servo motors with the adafruit HAT
        self.kit = ServoKit(channels = 16)
        self.kit.servo[0].set_pulse_width_range(400, 2350)
        self.kit.servo[1].set_pulse_width_range(385, 2300)
        self.kit.servo[0].angle, self.kit.servo[1].angle = 0, 0

    # Moving the stepper motor clockwise by changing coil current
    def move_right(self, steps):
        for i in range(steps):
            # Ensuring the output of the direction pin is equal to 1 or CW
            GPIO.output(DIR, CW)
            GPIO.output(STEP, GPIO.HIGH)
            sleep(DELAY)
            GPIO.output(STEP, GPIO.LOW)
            sleep(DELAY)

    # Moving left by moving counterclockwise
    def move_left(self, steps):
        for i in range(steps):
            # Ensuring the direction pin is set to 0 or CCW
            GPIO.output(DIR, CCW)
            GPIO.output(STEP, GPIO.HIGH)
            sleep(DELAY)
            GPIO.output(STEP, GPIO.LOW)
            sleep(DELAY)

    def face_detected(self):
        self.kit.servo[0].angle, self.kit.servo[1].angle = 90, 90
        sleep(1)
        self.kit.servo[0].angle, self.kit.servo[1].angle = 0, 0

    def cleanup(self):
        GPIO.cleanup()
        

class camera():
    def __init__(self, wanted_camera):
        self.wanted_camera = wanted_camera
        self.face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        self.mid_face_x = None

    # Finding faces 
    def start_video(self, turret):
        self.direction_of_motor = None

        while True:
            capture = cv2.VideoCapture(0)
            return_value, self.frame = capture.read()

            if return_value:
                end_y = self.frame.shape[0]
                self.mid_x = floor(self.frame.shape[1] / 2)

                # Detecting the face on a gray image to decrease processing time
                cv2.line(
                    self.frame,
                    (self.mid_x, 0),
                    (self.mid_x, end_y), 
                    (0, 255, 0), 
                    thickness = 10
                    )

                gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
                face = self.face_classifier.detectMultiScale(gray, 1.3, 5)

                # For the respective coords returned by the detectMultiScale
                for (x,y,w,h) in face:
                    self.mid_face_x = x + floor(w/2)

                    # Drawing the line of the middle of the face using a red line.
                    cv2.line(
                        self.frame, 
                        (self.mid_face_x, 0), 
                        (self.mid_face_x, end_y), 
                        (0,0,255), 
                        thickness=10
                        )

                    self.motor_checking(turret, mid_face_x = self.mid_face_x)
        
                cv2.imshow("Camera", self.frame)

                # Exit Sequence by waiting for esc
                k = cv2.waitKey(30) & 0xFF 
                if k == "27":
                    break

        turret.cleanup()

    def motor_checking(self, turret, mid_face_x = None):
        # Checking whether or not the kwarg mid_face_x was filled.
        if self.mid_face_x != None:
            # Checking the coordinates against the middle to see where we are currently 
            # CURRENT FORMULA => DISTANCE BETWEEN PIXELS DETECTED * 0.055625 * RESOLUTION(1/1, 1/2...)
            if self.mid_face_x < self.mid_x - 10:
                turret.move_left(floor(abs((self.mid_x - self.mid_face_x)) * 0.055625 / (RESOLUTION_CHOICE)))
            elif self.mid_face_x > self.mid_x + 10:
                turret.move_right(floor(abs((self.mid_x - self.mid_face_x)) * 0.055625 / (RESOLUTION_CHOICE)))
            else:
                turret.face_detected()
        else:
            return None