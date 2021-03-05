import cv2
import RPi.GPIO as GPIO
from time import sleep
from math import floor
from adafruit_servokit import ServoKit

# Creating a list to call from to move anticlockwise

sequence = [
    [1,0,0,1],
    [1,1,0,0],
    [0,1,1,0],
    [0,0,1,1]
]

# Creating a class for controlling the turret
class turret():
    def __init__(self, gpio_pins):

        # Setting up GPIO pins for the stepper motor
        self.gpio_pins = gpio_pins
        GPIO.setwarnings(False) 
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_pins, GPIO.OUT)

        # Resetting the coils to their first phase.
        GPIO.output(self.gpio_pins, (GPIO.HIGH, GPIO.LOW, GPIO.LOW, GPIO.HIGH))

        # Setting up the servo motors with the adafruit HAT
        self.kit = ServoKit(channels = 16)
        self.kit.servo[0].set_pulse_width_range(400, 2350)
        self.kit.servo[1].set_pulse_width_range(385, 2300)
        self.kit.servo[0].angle = 0
        self.kit.servo[1].angle = 0

    
    # Moving the stepper motor clockwise by changing coil current
    def move_right(self, steps):
        for i in range(steps):
            GPIO.output(self.gpio_pins, (GPIO.HIGH, GPIO.LOW, GPIO.LOW, GPIO.HIGH))
            sleep(0.04)
            GPIO.output(self.gpio_pins, (GPIO.HIGH, GPIO.HIGH, GPIO.LOW, GPIO.LOW))
            sleep(0.04)
            GPIO.output(self.gpio_pins, (GPIO.LOW, GPIO.HIGH, GPIO.HIGH, GPIO.LOW))
            sleep(0.04)
            GPIO.output(self.gpio_pins, (GPIO.LOW, GPIO.LOW, GPIO.HIGH, GPIO.HIGH))
            sleep(0.04)

    
    # Moving left by moving anticlockwise
    def move_left(self, steps):
        for i in range(steps):
            for step in reversed(range(len(sequence))):
                GPIO.output(self.gpio_pins[0], sequence[step][0])
                sleep(0.02)
                GPIO.output(self.gpio_pins[1], sequence[step][1])
                sleep(0.02)
                GPIO.output(self.gpio_pins[2], sequence[step][2])
                sleep(0.02)
                GPIO.output(self.gpio_pins[3], sequence[step][3])
                sleep(0.02)

    def face_detected(self):
        self.kit.servo[0].angle = 90
        self.kit.servo[1].angle = 90
        sleep(1)
        self.kit.servo[0].angle = 0
        self.kit.servo[1].angle = 0 

    
    def cleanup(self):
        GPIO.cleanup()
        

# Creating a class for the camera module 
class camera():
    def __init__(self, wanted_camera):
        self.wanted_camera = wanted_camera
        self.face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    

    # Finding faces 
    def start_video(self, turret):
        capture = cv2.VideoCapture(self.wanted_camera)

        while True:
            # Returning two values; if a value has been returned and the frame
            return_value, frame = capture.read()
            
            # Declaring some variables to clean up later.
            mid_x = floor(frame.shape[1] / 2)
            end_y = frame.shape[0]

            # Displaying the middle of the frame and coeffecient of 30
            cv2.line(frame, (mid_x + 30, 0), (mid_x + 30, end_y), (0, 255, 0), thickness = 10)

            # Detecting the face on a gray image to decrease processing time
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            face = self.face_classifier.detectMultiScale(gray, 1.3, 5)

            # For the respective coords returned by the detectMultiScale
            for (x,y,w,h) in face:
                mid_face_x = x + floor(w/2)

                # Drawing a line where the middle of the face is visually.
                cv2.line(frame, (mid_face_x, 0), (mid_face_x, end_y), (0,0,255), thickness=10)

                # Checking the coordinates against the middle to see where we are currently + 5 coeffecient
                if mid_face_x < mid_x - 10:
                    turret.move_right(1)
                elif mid_face_x > mid_x + 10:
                    turret.move_left(1)
                else:
                    turret.face_detected()
            
            # Displaying the actual video feed.
            cv2.imshow("Camera", frame)
        
            # Checking if the user wants to close the window
            k = cv2.waitKey(30) & 0xFF 
            if k == "27":
                break

        turret.cleanup()