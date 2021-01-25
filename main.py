import RPi.GPIO as GPIO
import time

class Windgong:

    def __init__(self):
        self.running = True
        self.button_pins = {}
        self.motor_pins = []
        # 0: Red_pin, 1: Green_pin
        self.led_pins = []
        # 0: off, 1: red, 2: green
        self.led_state = 0
        self.timeout = None
        self.holdtime = None
        self.target = None
        self.holding = False

        GPIO.setmode(GPIO.BCM)
    
    def createButton(self, name, channel):
        # the state can be '0' (if button pressed) or '1' (if button released)
        button_state = 1
        self.button_pins[name] = { "channel": channel, "state": button_state }

        # set pin GPIO4 to be an input pin; this pin will read the button state
        # activate pull down for pin GPIO4
        GPIO.setup(channel, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
    def createMotor(self, pin1, pin2, pin3, pin4):
        pins = [pin1, pin2, pin3, pin4]
        for pin in pins:
            self.motor_pins.append(pin)
            GPIO.setup(pin, GPIO.OUT)
            # Set all motor pins to low
            GPIO.output(pin, GPIO.LOW)
    
    def createLED(self, red_pin, green_pin):
        pins = [red_pin, green_pin]
        for pin in pins:
            self.led_pins.append(pin)
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.LOW)
        self.led_state = 0
    
    def setLED(self, color):
        if color == "green":
            GPIO.output(self.led_pins[0], GPIO.HIGH)
            GPIO.output(self.led_pins[1], GPIO.LOW)
            self.led_state = 2
        if color == "red":
            GPIO.output(self.led_pins[1], GPIO.HIGH)
            GPIO.output(self.led_pins[0], GPIO.LOW)
            self.led_state = 1
        if color == "off":
            GPIO.output(self.led_pins[0], GPIO.HIGH)
            GPIO.output(self.led_pins[0], GPIO.LOW)
            self.led_state = 0


    """
    @param clockwise: true for clockwise rotation, false for counter clockwise
    """
    def rotateMotor(self, clockwise):
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

        if len(self.motor_pins) != 0:
            for i in range(len(seq)):
                # Orange cable
                GPIO.output(self.motor_pins[0], seq[i][0])
                # Yellow cable
                GPIO.output(self.motor_pins[1], seq[i][1])
                # Pink cable
                GPIO.output(self.motor_pins[2], seq[i][2])
                # Blue cable
                GPIO.output(self.motor_pins[3], seq[i][3])

                # Set delay till next sequence
                time.sleep(2 / 1000)

    def checkButton(self):
        for button in self.button_pins:
            # read the current button state by reading pin GPIO4 on the Raspberry PI
            curr_state = GPIO.input(self.button_pins[button]["channel"])
            if curr_state != self.button_pins[button]["state"]:

                if curr_state == 1:
                    print(f"button '{button}' has been released")
                    # Add event

                if curr_state == 0:
                    print(f"button '{button}' has been pressed")
                    

                self.button_pins[button]["state"] = curr_state
    
    def checkTimeout(self):
        if self.timeout != None:
            if time.time() > self.timeout:
                self.timeout = None
    
    def setTarget(self, color):
        if color != self.target:
            timeout_time = 5
            hold_time = 5 + timeout_time
            self.timeout = time.time() + timeout_time
            self.holdtime = time.time() + hold_time
            self.setLED(color)
            print(f"PRESS {color}")
    
    def gameLogic(self):
        # If the led is red
        if self.led_state == 1:
            self.rotateMotor(True)
            if not self.timeout:
                red_state = self.button_pins["rood"]["state"]
                green_state = self.button_pins["groen"]["state"]

                if red_state == 0 and green_state != 0:
                    print("HOLD")
                    self.holding = True
                    if time.time() > self.holdtime:
                        self.setTarget("green")
                        self.holding = False
                else:
                    if green_state == 0 and red_state == 0:
                        print("Green was pressed aswell!")
                    if red_state != 0 and self.holding == False:
                        print("You were too late pressing the Red button")
                    if red_state != 0 and self.holding == True:
                        print("You released the Red button too early")

                    self.running = False

        # If the led is green
        if self.led_state == 2:
            self.rotateMotor(False)
            if not self.timeout:
                red_state = self.button_pins["rood"]["state"]
                green_state = self.button_pins["groen"]["state"]

                if green_state == 0 and red_state != 0:
                    print("HOLD")
                    self.holding = True
                    if time.time() > self.holdtime:
                        self.setTarget("red")
                        self.holding = False
                else:
                    if green_state == 0 and red_state == 0:
                        print("Red was pressed aswell!")
                    if green_state != 0 and self.holding == False:
                        print("You were too late pressing the Green button")
                    if green_state != 0 and self.holding == True:
                        print("You released the Green button too early")
                        
                    self.running = False
    
    def startGame(self):
        self.setTarget("red")
        while self.running:
            self.checkButton()
            self.gameLogic()
            self.checkTimeout()
            time.sleep(0.02)
        
        print("Game Ended")
        GPIO.cleanup()

if __name__ == "__main__":
    windgong = Windgong()
    # Red button
    windgong.createButton("rood", 14)
    # Green button
    windgong.createButton("groen", 15)
    # Blue button
    windgong.createButton("blauw", 4)
    
    # Motor
    windgong.createMotor(18,23,24,25)

    # Led
    windgong.createLED(27,22)

    windgong.startGame()