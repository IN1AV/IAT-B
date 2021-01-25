import RPi.GPIO as GPIO
import time

pins = []
motor_pins = []
def initialize():
    GPIO.setmode(GPIO.BCM)

def createButton(channel):
    # the state can be '0' (if button pressed) or '1' (if button released)
    button_state = 1
    pins.append([channel, button_state])

    # set pin GPIO4 to be an input pin; this pin will read the button state
    # activate pull down for pin GPIO4
    GPIO.setup(channel, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def createMotor(pin1, pin2, pin3, pin4):
    motor_pins = [pin1, pin2, pin3, pin4]
    # Set all motor pins to low
    GPIO.output(motor_pins, GPIO.LOW)

"""
@param: true for clockwise rotation, false for counter clockwise
"""
def rotateMotor(clockwise):
    if clockwise:
        seq = [
            [0,1,1,1],
            [0,0,1,1],
            [1,0,1,1],
            [1,0,0,1],
            [1,1,0,1],
            [1,1,0,0],
            [1,1,1,0],
            [0,1,1,0]
        ]
    else:
        seq = [
            [1,0,0,0],
            [1,1,0,0],
            [0,1,0,0],
            [0,1,1,0],
            [0,0,1,0],
            [0,0,1,1],
            [0,0,0,1],
            [1,0,0,1]
        ]
    if len(motor_pins) != 0:
        for i in range(len(seq)):
            # Orange cable
            GPIO.output(motor_pins[0], seq[i][0])
            # Yellow cable
            GPIO.output(motor_pins[1], seq[i][1])
            # Pink cable
            GPIO.output(motor_pins[2], seq[i][2])
            # Blue cable
            GPIO.output(motor_pins[3], seq[i][3])
    

def checkButton():
    for i in range(len(pins)):
            # read the current button state by reading pin GPIO4 on the Raspberry PI
            curr_state = GPIO.input(pins[i][0])
            if curr_state != pins[i][1]:
                if curr_state == 1:
                    print(f"GPIO{pins[i][0]} button released")
                    # Add event
                if curr_state == 0:
                    print(f"GPIO{pins[i][0]} button pressed")
                    # Add event
                pins[i][1] = curr_state

def gameLogic():
    return

def startGame():
    while True:
        checkButton()
        gameLogic()
        time.sleep(0.02)

if __name__ == "__main__":
    initialize()
    # Rode-knop
    createButton(14)
    # Groene-knop
    createButton(15)
    # Blauwe-knop
    createButton(4)

    startGame()