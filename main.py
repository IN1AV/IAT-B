import RPi.GPIO as GPIO
import time

pins = []

def initialize():
    GPIO.setmode(GPIO.BCM)

def createButton(channel):
    # the state can be '0' (if button pressed) or '1' (if button released)
    button_state = 1
    pins.append([channel, button_state])

    # set pin GPIO4 to be an input pin; this pin will read the button state
    # activate pull down for pin GPIO4
    GPIO.setup(channel, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def startListening():
    while True:
        for i in range(len(pins)):
            # read the current button state by reading pin GPIO4 on the Raspberry PI
            curr_state = GPIO.input(pins[i][0])
            if curr_state != pins[i][1]:
                if curr_state == 1:
                    print("button released")
                if curr_state == 0:
                    print("button pressed")
        time.sleep(0.02)

if __name__ == "__main__":
    initialize()
    createButton(4)
    createButton(17)
    startListening()