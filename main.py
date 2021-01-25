import RPi.GPIO as GPIO
import time

class Windgong:

    def __init__(self):
        self.running = True
        self.pins = []
        self.motor_pins = []
        self.timeout = time.time() + 5

        GPIO.setmode(GPIO.BCM)
    
    def createButton(self, channel):
        # the state can be '0' (if button pressed) or '1' (if button released)
        button_state = 1
        self.pins.append([channel, button_state])

        # set pin GPIO4 to be an input pin; this pin will read the button state
        # activate pull down for pin GPIO4
        GPIO.setup(channel, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
    def createMotor(self, pin1, pin2, pin3, pin4):
        motorpins = [pin1, pin2, pin3, pin4]
        for pin in motorpins:
            self.motor_pins.append(pin)
            GPIO.setup(pin, GPIO.OUT)
            # Set all motor pins to low
            GPIO.output(pin, GPIO.LOW)

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
        for i in range(len(self.pins)):
            # read the current button state by reading pin GPIO4 on the Raspberry PI
            curr_state = GPIO.input(self.pins[i][0])
            if curr_state != self.pins[i][1]:

                self.timeout = time.time() + 5

                if curr_state == 1:
                    print(f"GPIO{self.pins[i][0]} button released")
                    # Add event
                if curr_state == 0:
                    print(f"GPIO{self.pins[i][0]} button pressed")
                    # Add event
                self.pins[i][1] = curr_state
    
    def checkTimeout(self):
        if time.time() > self.timeout:
            self.running = False
    
    def gameLogic(self):
        # If the led is red
        # rotateMotor(true)
        # Check if the red button is pressed within time

        # If the led is green
        # rotateMotor(false)
        # Check if the green button is pressed within time

        return
    
    def startGame(self):
        while self.running:
            self.checkButton()
            self.gameLogic()
            self.rotateMotor(True)
            self.checkTimeout()
            time.sleep(0.02)
        
        print("TimeOut!")
        GPIO.cleanup()

if __name__ == "__main__":
    windgong = Windgong()
    # Red button
    windgong.createButton(14)
    # Green button
    windgong.createButton(15)
    # Blue button
    windgong.createButton(4)
    
    # Motor
    windgong.createMotor(18,23,24,25)

    windgong.startGame()