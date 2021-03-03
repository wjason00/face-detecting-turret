import cv2
import RPi.GPIO as GPIO
from time import sleep
from math import floor
from adafruit_servokit import ServoKit

# Creating a class
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
            GPIO.output(self.gpio_pins, (GPIO.HIGH, GPIO.HIGH, GPIO.LOW, GPIO.LOW))
            GPIO.output(self.gpio_pins, (GPIO.LOW, GPIO.HIGH, GPIO.HIGH, GPIO.LOW))
            GPIO.output(self.gpio_pins, (GPIO.LOW, GPIO.LOW, GPIO.HIGH, GPIO.HIGH))

    
    # Moving left by moving anticlockwise
    def move_left(self, steps):
        for i in range(steps):
            GPIO.output(self.gpio_pins, (GPIO.HIGH, GPIO.LOW, GPIO.LOW, GPIO.HIGH))
            GPIO.output(self.gpio_pins, (GPIO.LOW, GPIO.LOW, GPIO.HIGH, GPIO.HIGH))
            GPIO.output(self.gpio_pins, (GPIO.LOW, GPIO.HIGH, GPIO.HIGH, GPIO.LOW))
            GPIO.output(self.gpio_pins, (GPIO.HIGH, GPIO.HIGH, GPIO.LOW, GPIO.LOW))


    def face_detected(self):
        # Change this later so that it moves once and rotates 90 degrees
        for i in range(180):
            self.kit.servo[0].angle = 90
            self.kit.servo[1].angle = 90
            self.kit.servo[0].angle = 0
            self.kit.servo[1].angle = 0
            sleep(0.05)

    
    def cleanup(self):
        GPIO.cleanup()
        

# Creating a class for the camera module 
class camera():
    def __init__(self, wanted_camera):
        self.wanted_camera = wanted_camera
        self.face_classifier = cv2.CascadeClassifier("haarcascade_face.xml")
    

    # Finding faces 
    def start_video(self, turret):
        capture = cv2.VideoCapture(self.wanted_camera)

        while True:
            mid_x = floor(frame.shape[1] / 2)
            end_y = frame.shape[0]

            # Displaying the middle of the frame
            return_value, frame = capture.read()
            cv2.line(frame, (mid_x, 0), (mid_x, end_y), (0, 255, 0), thickness = 10)

            # Detecting the face on a gray image to decrease processing time
            grayscaled = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            face = self.face_classifier.detectMultiScale(grayscaled, 1.3, 5)

            # For the respective coords returned by the detectMultiScale
            for (x,y,w,h) in face:
                # Finding the middle of the face detected and rounding down.
                mid_x_face_coords = floor((x+w) / 2) 

                # Drawing a line where the middle of the face is visually.
                cv2.line(frame, (mid_x_face_coords, 0), (mid_x_face_coords, frame.shape[0]), (0,0,255), thickness=10)

                # Checking the coordinates against the middle to see where we are currently
                if mid_x_face_coords < mid_x:
                    turret.move_left(10)
                
                elif mid_x_face_coords > mid_x:
                    turret.move_right(10)

                else:
                    turret.face_detected()
            
            # Displaying the actual video feed.
            cv2.imshow("Camera", frame)

        
            # Checking if the user wants to close the window
            k = cv2.waitKey(30) & 0xFF 
            if k == "27":
                break

        turret.cleanup()







