# face-detecting-turret
## Plan

---

A turret run on a stepper motor that utilises a camera attachment and a raspberry pi. The overall idea is to use opencv2's library to use videocapture and then using the width of the screen we locate the middle of the screen and check it with a haar cascade box to which we find the middle and see if they line up. If they don't line up, then we move the stepper motor. 

The overall turret part of the project is going to be a piece of string attached to a servo motor. The overall turret (whatever I decide to make it) will be attached to a stepper motor which moves by an offset of x amount of steps in accordance to the amount of steps moved by the stepper motor with the camera module; e.g a follower and a leader type of scheme.

---

# Hardware
## Electronic Specifics

- Stepper Motor 
: 28YBJ-48

- Servo Motor
: SG90 

- Raspberry Pi 
: Model 4B / Pico (Might want to try out the Pico)

- Camera Module
: CAM-MIPI9281RAW (Made by Innomaker)

- Power Supply (For supplying power to the stepper motor and servos)
: Any 5-12V capable power supply will do.

- Servo Driver 
: Adafruit Waveshare Servo Driver 16 Channels (Any number of channels will do so long as it's above 4)

- Stepper Driver
: ULN2003 driver board

- Voltage Transistor (Turning 12V to 5V)
: L8075 Voltage Transistor 

- Capacitors (For minimising ripple across the voltage transistor)
: 10mF and 1mF capacitors capable of at least 12V

- Pigtail Power Connectors (For supplying 5V to the Servo Driver board)
: 2.1mm x 5.5mm Male and Female DC Pigtal Power Connectors 12V capable.

## 3D Models

![image](https://user-images.githubusercontent.com/70390694/109780429-eba06880-7bfe-11eb-9a68-1067510ce99e.png)
![image](https://user-images.githubusercontent.com/70390694/109780941-5fdb0c00-7bff-11eb-9955-9ed85b9b72c4.png)
![image](https://user-images.githubusercontent.com/70390694/109781071-80a36180-7bff-11eb-82d0-6d21a4a10be1.png)
![image](https://user-images.githubusercontent.com/70390694/109781225-a29ce400-7bff-11eb-9c66-27cd568abac7.png)

- A model for containing the 28BYJ-48 Stepper Motor and holding the camera module. 

![image](https://user-images.githubusercontent.com/70390694/109780563-0a9efa80-7bff-11eb-927e-6f1b737599c5.png)
![image](https://user-images.githubusercontent.com/70390694/109781276-ae88a600-7bff-11eb-8bb8-93e0ceb98c2a.png)
![image](https://user-images.githubusercontent.com/70390694/109781305-b47e8700-7bff-11eb-9aeb-3a362bdb5d82.png)

- A model for screwing the camera module into (2mm threads RIGHT HANDED)

![image](https://user-images.githubusercontent.com/70390694/109780768-37eba880-7bff-11eb-84eb-cd5c5b1aa9c9.png)
![image](https://user-images.githubusercontent.com/70390694/109780809-41751080-7bff-11eb-90db-48b3d71d9183.png)
![image](https://user-images.githubusercontent.com/70390694/109780858-4c2fa580-7bff-11eb-92de-a6c1cba00a08.png)
![image](https://user-images.githubusercontent.com/70390694/109780881-518cf000-7bff-11eb-9b90-d8ad49699026.png)

- A model for holding the servo motors and attaching itself to the stepper motor using a cylinder with radius of 6.75mm and shelled.

## Wiring
### Stepper Motor

The stepper motor has to be wired into the ULN2003 Driver Board and this board takes in VIM and GND from an external power supply and they have the 4 coils of the bipolar 28BYJ-48 connected to 4 GPIO pins. VIM is 5 volts to 12 volts and is shown by a "+" and ground is shown by "-" on the board.

The GPIO pins you choose should be consistent throughout the coding and should default as a tuple following the order of:

```
{
  "pin_1": 2,
  "pin_2": 3,
  "pin_3": 4,
  "pin_4": 14
}
```

> Note, use GPIO.BCM (Broadcom) which basically means that you're using the numbers following GPIO in the GPIO layout data sheet.

(INSERT PHOTO HERE OF ULN2003 BOARD WIRED)

### Servo Motor

The servo motor in this case is the Adafruit Waveshare Servo Driver w/ 16 channels and basically it's colour coded to match the colours of the wires of the servo motor with ground, signal and power representing brown, yellow and red respectively. External power supply must also be connected using the terminal blocks and this should only be 5V. If you use a 12V power supply, use a L8075 Voltage Transistor to step down the voltage by putting in 12 V at pin 1, connecting ground to pin 2 and then the output will be pin 3. Don't forget to connect resistors to reduce ripple and potentially destroy any of the circuit.
