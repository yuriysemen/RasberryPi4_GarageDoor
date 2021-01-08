import enum

import gpiozero

from app.doorControl.ThreeWayActivator import ThreeWayActivatorThread


class DoorStateEnum(enum.Enum):
    OPENED="opened",
    CLOSED="closed",
    OPERATING="operating",
    HALF_OPENED="halfOpened"


MOTOR_ACTIVATOR_PIN = 26


class Door:

    def __init__(self):
        self.state = DoorStateEnum.HALF_OPENED
        self.threeWayActivatorThread = ThreeWayActivatorThread(gpiozero.LED(active_high=False, pin=MOTOR_ACTIVATOR_PIN))
        self.threeWayActivatorThread.start()

        self.internalControlButton = gpiozero.Button(pin=4, pull_up=False)
        self.internalControlButton.when_pressed = self.activate

        self.door_locker = gpiozero.LED(pin=21, active_high=False, initial_value=True)

    def activate(self):
        self.threeWayActivatorThread.activate()