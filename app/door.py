import gpiozero
import time


class Door:

    def __init__(self):
        self.state = "closed"
        self.doorActivator = gpiozero.LED(active_high=False, pin=26)
        self.internalControlButton = gpiozero.Button(2)
        self.internalControlButton.when_pressed = self.internal_control_pressed
        self.internalControlButton.when_released = self.internal_control_released

    def internal_control_released(self):
        self.doorActivator.off()

    def internal_control_pressed(self):
        self.doorActivator.on()

    def open(self):
        self.state = "closing"
        self.doorActivator.on()
        time.sleep(1)
        self.doorActivator.off()
