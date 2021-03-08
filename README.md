# face-detecting-turret
## Plan

---

A turret run on a stepper motor that utilises a camera attachment and a raspberry pi. The overall idea is to use opencv2's library to use videocapture and then using the width of the screen we locate the middle of the screen and check it with a haar cascade box to which we find the middle and see if they line up. If they don't line up, then we move the stepper motor. 

The overall turret part of the project is going to be a piece of string attached to a servo motor. The overall turret (whatever I decide to make it) will be attached to a stepper motor which moves by an offset of x amount of steps in accordance to the amount of steps moved by the stepper motor with the camera module; e.g a follower and a leader type of scheme.

---

# Hardware
## Electronic Specifics

**- Stepper Motor 
: [28YBJ-48](https://www.amazon.co.uk/Elegoo-28BYJ-48-Stepper-ULN2003-Arduino/dp/B01LXT5740/ref=sr_1_8?crid=9NKB03MF57TH&dchild=1&keywords=28byj-48&qid=1614794453&sprefix=28BYJ+%2Caps%2C158&sr=8-8)**

**- Servo Motor
: [SG90](https://www.amazon.co.uk/Dawa-Helicopter-Airplane-Remote-Control/dp/B07MHFVBNN/ref=sr_1_14?dchild=1&keywords=Servo+Motor&qid=1614794502&sr=8-14)**

**- Raspberry Pi 
: [Model 4B](https://thepihut.com/products/raspberry-pi-4-model-b) / [Pico](https://thepihut.com/products/raspberry-pi-pico) (Might want to try out the [Pico](https://thepihut.com/products/raspberry-pi-pico))**

**- Camera Module
: [CAM-MIPI9281RAW](https://www.amazon.co.uk/Inno-Maker-Camera-Module-OV5647-Raspberry/dp/B07G9VLPZH/ref=sr_1_5?dchild=1&keywords=Raspberry+Pi+Camera+innomaker&qid=1614794603&sr=8-5) (Made by Innomaker)**

**- Power Supply (For supplying power to the stepper motor and servos)
: Any 5-12V capable power supply will do.**

**- Servo Driver 
: [Adafruit Waveshare Servo Driver 16 Channels](https://www.amazon.co.uk/Waveshare-16-Channel-Servo-Driver-HAT/dp/B07GYFTKZD/ref=sr_1_3?dchild=1&keywords=Servo+Driver+HAT&qid=1614794863&sr=8-3) (Any number of channels will do so long as it's above 4)**

**- Stepper Driver
: [ULN2003 driver board](https://www.amazon.co.uk/Elegoo-28BYJ-48-Stepper-ULN2003-Arduino/dp/B01LXT5740/ref=sr_1_8?crid=9NKB03MF57TH&dchild=1&keywords=28byj-48&qid=1614794453&sprefix=28BYJ+%2Caps%2C158&sr=8-8)**

**- Voltage Transistor (Turning 12V to 5V)
: [L8075 Voltage Transistor](https://www.amazon.co.uk/ARCELI-LM317T-L7824-Transistor-Assortment-Transistors/dp/B07NPQGXY2/ref=sr_1_5?dchild=1&keywords=voltage+transistor&qid=1614794701&sr=8-5)**

**- Capacitors (For minimising ripple across the voltage transistor)
: [10mF and 1mF capacitors capable of at least 12V](https://www.amazon.co.uk/ARCELI-15Value-Electrolytic-Capacitor-Assortment/dp/B07RN3Q8SD/ref=sr_1_5?dchild=1&keywords=capacitor+kit&qid=1614794760&sr=8-5)**

**- Pigtail Power Connectors (For supplying 5V to the Servo Driver board)
: [2.1mm x 5.5mm Male and Female DC Pigtal Power Connectors 12V capable.](https://www.amazon.co.uk/Pigtail-Security-Camera-Female-Connectors-Black/dp/B07Q9Z5PLL/ref=sr_1_5?dchild=1&keywords=Pigtail+connectors+5.5mm&qid=1614794788&sr=8-5)**

## 3D Models
### 28BYJ-48 Stepper Motor Holder
------------------------------

![image](https://user-images.githubusercontent.com/70390694/109851604-c84fda80-7c4b-11eb-867a-df5dc6820a34.png)
![image](https://user-images.githubusercontent.com/70390694/109780941-5fdb0c00-7bff-11eb-9955-9ed85b9b72c4.png)
![image](https://user-images.githubusercontent.com/70390694/109781071-80a36180-7bff-11eb-82d0-6d21a4a10be1.png)
![image](https://user-images.githubusercontent.com/70390694/109781225-a29ce400-7bff-11eb-9c66-27cd568abac7.png)

### Camera Module Holder
------------------------------

![image](https://user-images.githubusercontent.com/70390694/109851878-149b1a80-7c4c-11eb-8593-e0abaf3c389a.png)
![image](https://user-images.githubusercontent.com/70390694/109852046-43b18c00-7c4c-11eb-9be7-605237e79e2b.png)
![image](https://user-images.githubusercontent.com/70390694/109852113-55932f00-7c4c-11eb-9c9c-f39fa2dfd55b.png)

### Servo Motor Connector
------------------------------
![image](https://user-images.githubusercontent.com/70390694/109853174-8889f280-7c4d-11eb-83a5-724b8d6812e6.png)
![image](https://user-images.githubusercontent.com/70390694/109853225-963f7800-7c4d-11eb-876d-8c1aa7427939.png)
![image](https://user-images.githubusercontent.com/70390694/109853266-9f304980-7c4d-11eb-8dcb-ea527f265042.png)
![image](https://user-images.githubusercontent.com/70390694/109853297-ab1c0b80-7c4d-11eb-8a71-fcad2e895439.png)
![image](https://user-images.githubusercontent.com/70390694/109853344-b707cd80-7c4d-11eb-945f-372aa736c6fc.png)



## Wiring
### Stepper Motor

The stepper motor has to be wired into the ULN2003 Driver Board and this board takes in VIM and GND from an external power supply and they have the 4 coils of the bipolar 28BYJ-48 connected to 4 GPIO pins. VIM is 5 volts to 12 volts and is shown by a "+" and ground is shown by "-" on the board.

> The GPIO pins you choose should be consistent throughout the coding and should default as a tuple following the order of:

GPIO PIN | INPUT PIN (ON THE BOARD)
:----------: | :----------:
GPIO PIN 1 | IN1
GPIO PIN 2 | IN2
GPIO PIN 3 | IN3
GPIO PIN 4 | IN4 

> Note, use GPIO.BCM (Broadcom) which basically means that you're using the numbers following GPIO in the GPIO layout data sheet.

- The GPIO pins are connected to the following IN1, IN2, IN3, IN4 and these are named in the order of the coil they represent.
![ULN2003 Driver Board 1](https://user-images.githubusercontent.com/70390694/109843684-3e9c0f00-7c43-11eb-8e9d-a39f3b0e1fe8.jpg)

- A side view which shows the 5-12V ground and vin connections which are clearly shown by the **-** and **+** next to the female header.
![ULN2003 Driver Board 2](https://user-images.githubusercontent.com/70390694/109843704-4491f000-7c43-11eb-9802-a2918cf3cf19.jpg)



### Servo Motor

The servo motor in this case is the Adafruit Waveshare Servo Driver w/ 16 channels and basically it's colour coded to match the colours of the wires of the servo motor with:

Colour | Meaning | Colour Variations
:---: | :---: | :---:
Red | Power / Voltage | Orange
Yellow | Signal to control the direction | 
Brown | Ground | Black

External power supply must also be connected using the terminal blocks and this should only be 5V. If you use a 12V power supply, use a L8075 Voltage Transistor to step down the voltage by putting in 12 V at pin 1, connecting ground to pin 2 and then the output will be pin 3. Don't forget to connect resistors to reduce ripple and potentially destroy any of the circuit.

- 5.5mm x 2.2mm Pigtail Jack Connector into Terminal Block section and Male Jack
![5 5MM X 2 2MM Pigtail Connection 5V Terminal BLock](https://user-images.githubusercontent.com/70390694/109845715-596f8300-7c45-11eb-88dc-06f4150170f7.jpg)
![Male and Female Pigtail Connections](https://user-images.githubusercontent.com/70390694/109853969-66dd3b00-7c4e-11eb-9299-8effb171f137.jpg)

  - Used to supply the servo driver 5V and **ONLY** 5V. Supplying extra will most likely fry your I2C GPIO3 pin as I've experienced before and that's permanent. 

- L7085 Voltage Transistor 
![L8075 Transistor Breadboard Wiring](https://user-images.githubusercontent.com/70390694/109856511-78741200-7c51-11eb-8555-d406c3005648.jpg)

PINS | MEANING
:-----: | :-------:
1 (Connected to the yellow wire) | INPUT FROM 6V TO 15V
2 (Connected to the black wire) | GROUND 
3 (Connected to the red wire) | OUTPUT OF 5V

> These pin values are assuming from the front of the voltage transistor and to find the front, simply find the side with the text on stating what voltage transistor and other information.

### Camera Module 

The camera module comes with two ribbon cables (thin cables with traces on them that are durable as well). The ribbon cables that are supplied with will contain two sides, one of which is clearly dictated by a blue separating at the bottom. To insert the camera module, grab the sides of the camera module on the raspberry pi (a white rectangle with black sides) and carefully lift it up, once it has been lift up, pull it towards the ethernet ports and hdmi ports. Once this has been done, insert the blue side of the ribbon cable facing the ethernet ports and insert the ribbon cable. Once inserted, close the black sides by pulling them together. Do the same for the camera module.

-----------------

## Software
### Dependencies

Package Name | Version used | Pre-installed on Raspberry Pi 4B+ | 
:------------: | :------------: | :---------------------------------: | 
[OpenCV](https://pypi.org/project/opencv-python/) | 4.5.1.48 | NO
[RPi.GPIO](https://pypi.org/project/RPi.GPIO/) | 0.7.0 | YES
[adafruit_servokit](https://pypi.org/project/adafruit-circuitpython-servokit/) | 1.3.3 | NO
[math](https://www.python.org/downloads/) | 3.7.0 | YES 
[time](https://www.python.org/downloads/) | 3.7.0 | YES
[asyncio](https://pypi.org/project/asyncio/) | 3.4.3 | NO

> The Python version I used was 3.7.
