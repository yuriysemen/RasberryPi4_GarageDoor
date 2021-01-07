import enum
import time

import gpiozero
from app.doorControl.ThreeWayActivator import ThreeWayActivator


class DoorStateEnum(enum.Enum):
    OPENED="opened",
    CLOSED="closed",
    OPERATING="operating",
    HALF_OPENED="halfOpened"


class Door:

    def __init__(self):
        self.state = DoorStateEnum.HALF_OPENED
        self.threeWayActivator = ThreeWayActivator(pin=26)

        self.internalControlButton = gpiozero.Button(pin=4, pull_up=False)
        self.internalControlButton.when_pressed = self.internal_control_pressed

        self.door_locker = gpiozero.LED(pin=21, active_high=False, initial_value=True)

    def internal_control_pressed(self):
        self.door_locker.off()
        time.sleep(1)
        self.threeWayActivator.push()
        time.sleep(1)
        self.door_locker.on()
