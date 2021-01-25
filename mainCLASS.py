import RPi.GPIO as GPIO
import time


class TurkijeMotor:
    def __init__(self):
        self.pins = []

        GPIO.setmode(GPIO.BCM)

    def create_button (self, channel):
        # the state can be '0' (if button pressed) or '1' (if button released)
        button_state = 1
        self.pins.append([channel, button_state])

        # set pin GPIO4 to be an input pin; this pin will read the button state
        # activate pull down for pin GPIO4
        GPIO.setup(channel, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def listen(self):
        pins = self.pins

        # Times out after 60 seconds
        timeout = time.time() + 60

        print("Listening!")

        while True:
            if time.time() > timeout:
                break

            for i in range(len(pins)):
                # read the current button state by reading pin GPIO4 on the Raspberry PI
                curr_state = GPIO.input(pins[i][0])
                if curr_state != pins[i][1]:
                    if curr_state == 1:
                        print(f"GPIO{pins[i][0]} button released")
                    if curr_state == 0:
                        print(f"GPIO{pins[i][0]} button pressed")
                    pins[i][1] = curr_state
            time.sleep(0.02)


if __name__ == "__main__":
    turkije_motor = TurkijeMotor()
    turkije_motor.create_button(4)
    turkije_motor.create_button(17)
    turkije_motor.listen()
