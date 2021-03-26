DIR = 13 # SENDING THE DIRECTION PIN 13
STEP = 6 # CONTROLLING AND PULSING FROM GPIO 6
CW = 1 # CLOCKWISE = ON
CCW = 0 # COUNTERCLOCKWISE = OFF
SPR = 200  * (1 / (1/2))# STEPS PER REVOLUTION * (1 * (RESOLUTION))
DELAY = .005  / (1 / (1/1))# DELAY / (1 * (RESOLUTION))

# MICROSTEPPING 
MS_PINS = (10, 9, 11)
RESOLUTION = {
    1/1  : (0, 0, 0),
    1/2  : (1, 0, 0),
    1/4  : (0, 1, 0),
    1/8  : (1, 1, 0),
    1/16 : (0, 0, 1),
    1/32 : (1, 1, 1) # 1/32 has multiple values but I chose 1,1,1
    }
