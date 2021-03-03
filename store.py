import cv2
import RPi.GPIO as GPIO
from time import sleep
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
        mid_x = round(frame.shape[1] / 2)
        end_y = frame.shape[0]

        while True:
            # Displaying the middle of the frame
            return_value, frame = capture.read()
            cv2.line(frame, (mid_x, 0), (mid_x, end_y), (0, 255, 0), thickness = 10)

            # Detecting the face on a gray image to decrease processing time
            grayscaled = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            face = self.face_classifier.detectMultiScale(grayscaled, 1.3, 5)

            # For the respective coords returned by the detectMultiScale
            for (x,y,w,h) in face:
                mid_x_face_coords = round((x+y))







