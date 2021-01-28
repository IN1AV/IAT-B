import RPi.GPIO as GPIO
import time
import random

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
        self.clockwise = True
        self.previous_color = None

        self.minimum_delay = 2
        self.maximum_delay = 5
        self.time_to_hit_button = 1
        self.times_hit = 0

        self.points = 0
        self.reaction_time = 0
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
    
    # HIGH = HIGH
    # LOW = ON
    # Atleast that is what i think
    def setLED(self, color):
        if color == "green":
            self.previous_color = "green"
            self.clockwise = True
            GPIO.output(self.led_pins[0], GPIO.LOW)
            GPIO.output(self.led_pins[1], GPIO.HIGH)
            self.led_state = 2
        if color == "red":
            self.previous_color = "red"
            self.clockwise = False
            GPIO.output(self.led_pins[0], GPIO.HIGH)
            GPIO.output(self.led_pins[1], GPIO.LOW)
            self.led_state = 1
        if color == "off":
            GPIO.output(self.led_pins[0], GPIO.LOW)
            GPIO.output(self.led_pins[1], GPIO.LOW)
            self.led_state = 0

        print(f"LED COLOR: {color}")


    """
    @param clockwise: true for clockwise rotation, false for counter clockwise
    """
    def rotateMotor(self, clockwise):
        # if clockwise:
        #     seq = [
        #         [0,1,1,1],
        #         [0,0,1,1],
        #         [1,0,1,1],
        #         [1,0,0,1],
        #         [1,1,0,1],
        #         [1,1,0,0],
        #         [1,1,1,0],
        #         [0,1,1,0]
        #     ]
        # else:
        #     # seq = [
        #     #     [1,0,0,0],
        #     #     [1,1,0,0],
        #     #     [0,1,0,0],
        #     #     [0,1,1,0],
        #     #     [0,0,1,0],
        #     #     [0,0,1,1],
        #     #     [0,0,0,1],
        #     #     [1,0,0,1]
        #     # ]

        if clockwise:
            seq = [
                [1,1,0,0],
                [0,1,1,0],
                [0,0,1,1],
                [1,0,0,1]
            ]
        else:
            seq = [
                [1,0,0,1],
                [0,0,1,1],
                [0,1,1,0],
                [1,1,0,0]
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
                time.sleep(5 / 1000)
                # time.sleep(5/1000)

    def checkButton(self):
        for button in self.button_pins:
            # read the current button state by reading pin GPIO4 on the Raspberry PI
            curr_state = GPIO.input(self.button_pins[button]["channel"])
            if curr_state != self.button_pins[button]["state"]:

                # if curr_state == 1:
                #     print(f"button '{button}' has been released")
                #     # Add event

                # if curr_state == 0:
                #     print(f"button '{button}' has been pressed")
                    

                self.button_pins[button]["state"] = curr_state
    
    def checkTimeout(self):
        if self.timeout != None:
            if time.time() > self.timeout:
                self.timeout = None
    
    def setTarget(self, color):
        self.timeout = time.time() + self.time_to_hit_button
        self.setLED(color)
        print(f"PRESS {color}")
    
    def gameLogic(self):
        red_state = self.button_pins["rood"]["state"]
        green_state = self.button_pins["groen"]["state"]
        # If the led is red
        if self.timeout != None:
            # red
            if self.led_state == 1:
                if red_state == 0 and green_state != 0:
                    self.holding = True
                if green_state == 0:
                    print("You pressed the wrong button")
                    self.running = False

            # green
            if self.led_state == 2:
                if red_state != 0 and green_state == 0:
                    self.holding = True

                if red_state == 0:
                    print("You pressed the wrong button")
                    self.running = False
            
            if self.holding:
                # Reduce time it takes to switch led
                self.minimum_delay /= 1.1
                self.maximum_delay /= 1.1
                # Reduce time the player has to hit correct button
                self.time_to_hit_button /= 1.1
                self.times_hit += 1
                self.reaction_time = self.timeout - time.time()
                # Code here for point system based on reaction time
                self.points = self.points + self.reaction_time * self.times_hit
                print(f"Hits: {self.times_hit}, Points: {self.points}")

                self.timeout = None
                self.holdtime = time.time() + random.uniform(self.minimum_delay, self.maximum_delay)
                # Key Debounce Time of 500ms
                self.debouncetime = time.time() + 0.5
                self.setLED("off")


        if self.timeout == None and self.holding:
            if time.time() > self.holdtime:
                self.holdtime = None
                if self.previous_color == "green":
                    self.setTarget("red")
                else:
                    self.setTarget("green")
                # color = ["green", "red"]
                # self.setTarget(color[random.randint(0, 1)])
                self.holding = False
            else:
                if time.time() > self.debouncetime:
                    if red_state == 0 or green_state == 0:
                        print("You pressed when the LED was off")
                        self.running = False
        
        if self.timeout == None and not self.holding :
            print("You were too late")
            self.running = False
        
        self.rotateMotor(self.clockwise)

    def startGame(self):
        self.setTarget("green")
        while self.running:
            self.checkButton()
            self.gameLogic()
            self.checkTimeout()

            # ~60 updates per second
            # time.sleep(0.02)
        
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