# Face-detecting turret

## Overview

A stepper-motor-driven turret built on a Raspberry Pi with a camera module that tracks faces in real time.  
OpenCV’s `VideoCapture` captures frames, a Haar cascade detects faces, and the face-box centre is compared to the frame centre; if they do not align, the stepper motor is rotated to reduce the error.

The turret mechanism is driven by a servo (for the “firing” or pointing action) mounted on a stepper-motor platform.  
The stepper that holds the camera acts as the “leader”, and the turret stepper follows with a fixed step offset.

---

## Hardware

### Electronic components

- **Stepper motor:** [28BYJ-48](https://www.amazon.co.uk/Elegoo-28BYJ-48-Stepper-ULN2003-Arduino/dp/B01LXT5740/ref=sr_1_8?crid=9NKB03MF57TH&dchild=1&keywords=28byj-48&qid=1614794453&sprefix=28BYJ+%2Caps%2C158&sr=8-8)
- **Servo motor:** [SG90](https://www.amazon.co.uk/Dawa-Helicopter-Airplane-Remote-Control/dp/B07MHFVBNN/ref=sr_1_14?dchild=1&keywords=Servo+Motor&qid=1614794502&sr=8-14)
- **Raspberry Pi:** [Model 4B](https://thepihut.com/products/raspberry-pi-4-model-b) or [Pico](https://thepihut.com/products/raspberry-pi-pico)
- **Camera module:** [CAM-MIPI9281RAW](https://www.amazon.co.uk/Inno-Maker-Camera-Module-OV5647-Raspberry/dp/B07G9VLPZH/ref=sr_1_5?dchild=1&keywords=Raspberry+Pi+Camera+innomaker&qid=1614794603&sr=8-5) (Innomaker)
- **Power supply:** 5–12 V DC for stepper motor and servos
- **Servo driver:** [16‑channel servo driver HAT](https://www.amazon.co.uk/Waveshare-16-Channel-Servo-Driver-HAT/dp/B07GYFTKZD/ref=sr_1_3?dchild=1&keywords=Servo+Driver+HAT&qid=1614794863&sr=8-3) (≥ 4 channels)
- **Stepper driver:** [ULN2003 driver board](https://www.amazon.co.uk/Elegoo-28BYJ-48-Stepper-ULN2003-Arduino/dp/B01LXT5740/ref=sr_1_8?crid=9NKB03MF57TH&dchild=1&keywords=28byj-48&qid=1614794453&sprefix=28BYJ+%2Caps%2C158&sr=8-8)
- **Voltage regulator (12 V → 5 V):** [L8075](https://www.amazon.co.uk/ARCELI-LM317T-L7824-Transistor-Assortment-Transistors/dp/B07NPQGXY2/ref=sr_1_5?dchild=1&keywords=voltage+transistor&qid=1614794701&sr=8-5)
- **Capacitors (smoothing):** 10 mF and 1 mF electrolytics (≥ 12 V rating)
- **Pigtail connectors:** [2.1 mm × 5.5 mm DC pigtails](https://www.amazon.co.uk/Pigtail-Security-Camera-Female-Connectors-Black/dp/B07Q9Z5PLL/ref=sr_1_5?dchild=1&keywords=Pigtail+connectors+5.5mm&qid=1614794788&sr=8-5) for 5 V into the servo driver

---

## 3D models

> All images are scaled using HTML `<img>` tags so they render with a consistent width in GitHub/Obsidian.

### 28BYJ‑48 stepper motor holder

<div align="center">
  <img src="https://user-images.githubusercontent.com/70390694/109851604-c84fda80-7c4b-11eb-867a-df5dc6820a34.png" alt="28BYJ-48 Holder 1" width="320" />
  <img src="https://user-images.githubusercontent.com/70390694/109780941-5fdb0c00-7bff-11eb-9955-9ed85b9b72c4.png" alt="28BYJ-48 Holder 2" width="320" />
  <img src="https://user-images.githubusercontent.com/70390694/109781071-80a36180-7bff-11eb-82d0-6d21a4a10be1.png" alt="28BYJ-48 Holder 3" width="320" />
  <img src="https://user-images.githubusercontent.com/70390694/109781225-a29ce400-7bff-11eb-9c66-27cd568abac7.png" alt="28BYJ-48 Holder 4" width="320" />
</div>

### Camera module holder

<div align="center">
  <img src="https://user-images.githubusercontent.com/70390694/109851878-149b1a80-7c4c-11eb-8593-e0abaf3c389a.png" alt="Camera Holder 1" width="320" />
  <img src="https://user-images.githubusercontent.com/70390694/109852046-43b18c00-7c4c-11eb-9be7-605237e79e2b.png" alt="Camera Holder 2" width="320" />
  <img src="https://user-images.githubusercontent.com/70390694/109852113-55932f00-7c4c-11eb-9c9c-f39fa2dfd55b.png" alt="Camera Holder 3" width="320" />
</div>

### Servo motor connector

<div align="center">
  <img src="https://user-images.githubusercontent.com/70390694/109853174-8889f280-7c4d-11eb-83a5-724b8d6812e6.png" alt="Servo Connector 1" width="320" />
  <img src="https://user-images.githubusercontent.com/70390694/109853225-963f7800-7c4d-11eb-876d-8c1aa7427939.png" alt="Servo Connector 2" width="320" />
  <img src="https://user-images.githubusercontent.com/70390694/109853266-9f304980-7c4d-11eb-8dcb-ea527f265042.png" alt="Servo Connector 3" width="320" />
  <img src="https://user-images.githubusercontent.com/70390694/109853297-ab1c0b80-7c4d-11eb-8a71-fcad2e895439.png" alt="Servo Connector 4" width="320" />
  <img src="https://user-images.githubusercontent.com/70390694/109853344-b707cd80-7c4d-11eb-945f-372aa736c6fc.png" alt="Servo Connector 5" width="320" />
</div>

---

## Wiring

### Stepper motor

The 28BYJ‑48 connects to the ULN2003 driver board, which is powered from an external 5–12 V supply on VIN and GND.  
The four driver inputs IN1–IN4 each connect to a dedicated Raspberry Pi GPIO pin.

> Use `GPIO.BCM` numbering and keep the pin mapping consistent in code (e.g. `(IN1, IN2, IN3, IN4)`).

GPIO PIN | INPUT PIN (ULN2003)
:----------: | :----------:
GPIO PIN 1 | IN1
GPIO PIN 2 | IN2
GPIO PIN 3 | IN3
GPIO PIN 4 | IN4

<div align="center">
  <img src="https://user-images.githubusercontent.com/70390694/109843684-3e9c0f00-7c43-11eb-8e9d-a39f3b0e1fe8.jpg" alt="ULN2003 Front" width="360" />
  <img src="https://user-images.githubusercontent.com/70390694/109843704-4491f000-7c43-11eb-9802-a2918cf3cf19.jpg" alt="ULN2003 Side" width="360" />
</div>

### Servo motor

The servo is driven from the 16‑channel servo driver HAT.  
Wire colours map as:

Colour | Meaning | Variants
:---: | :---: | :---:
Red | V+ / power | Orange
Yellow | Signal (PWM) | –
Brown | Ground | Black

Use a 5 V external supply into the HAT’s terminal block for the servos.  
If your main supply is 12 V, convert it to 5 V using an L8075 regulator with decoupling capacitors.

<div align="center">
  <img src="https://user-images.githubusercontent.com/70390694/109845715-596f8300-7c45-11eb-88dc-06f4150170f7.jpg" alt="Pigtail to Terminal Block" width="360" />
  <img src="https://user-images.githubusercontent.com/70390694/109853969-66dd3b00-7c4e-11eb-9299-8effb171f137.jpg" alt="Male and Female Pigtails" width="360" />
</div>

- Only supply 5 V to the servo driver; higher voltages can permanently damage I²C pins and servos.

L8075 example:

<div align="center">
  <img src="https://user-images.githubusercontent.com/70390694/109856511-78741200-7c51-11eb-8555-d406c3005648.jpg" alt="L8075 Wiring" width="360" />
</div>

PINS | Meaning
:-----: | :-------:
1 (yellow wire) | Input 6–15 V
2 (black wire) | Ground
3 (red wire) | 5 V output

> Pin numbering is from the front of the regulator (side with printed text).

### Camera module

The camera module uses a ribbon cable with a blue stiffener on one side.  
On the Raspberry Pi, lift the camera connector latch, pull it towards the Ethernet/HDMI ports, insert the ribbon with the blue side facing the Ethernet ports, and close the latch.  
Repeat on the camera PCB, again matching ribbon orientation.

---

## Software

### Dependencies

Package | Version | Pre‑installed on Pi 4B+
:------------: | :------------: | :---------------------------------:
[OpenCV](https://pypi.org/project/opencv-python/) | 4.5.1.48 | NO
[RPi.GPIO](https://pypi.org/project/RPi.GPIO/) | 0.7.0 | YES
[adafruit_servokit](https://pypi.org/project/adafruit-circuitpython-servokit/) | 1.3.3 | NO
[math](https://www.python.org/downloads/) | 3.7.0 | YES
[time](https://www.python.org/downloads/) | 3.7.0 | YES
[asyncio](https://pypi.org/project/asyncio/) | 3.4.3 | NO

> Python version used: 3.7.
