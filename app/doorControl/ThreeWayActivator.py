import enum
import threading
import time

import gpiozero


class ThreeWayActivatorStateEnum(enum.Enum):
    IDLE = "idle",
    ACTIVE = "active",
    COOL_DOWN = "coolDown"


class ActivatorThread(threading.Thread):

    def __init__(self, activator, progress_listener):
        super().__init__()
        self.activator = activator
        self.progressListener = progress_listener

    def run(self):
        self.activator.on()
        self.progressListener(ThreeWayActivatorStateEnum.ACTIVE)

        time.sleep(1)

        self.activator.off()
        self.progressListener(ThreeWayActivatorStateEnum.COOL_DOWN)

        time.sleep(1)
        self.progressListener(ThreeWayActivatorStateEnum.IDLE)


class ThreeWayActivator:

    def __init__(self, pin: int):
        self.pin = pin
        self.activator = gpiozero.LED(active_high=False, pin=pin)
        self.lock = threading.Lock()

        self.state = "IDLE"
        print(self.state)

    def state_changed(self, new_state):
        self.lock.acquire()
        try:
            self.state = new_state
            print(self.state)
        finally:
            self.lock.release()

    def push(self):
        self.lock.acquire()
        try:
            if self.state == "IDLE":
                thread = ActivatorThread(activator=self.activator, progress_listener=self.state_changed)
                thread.start()
                print(self.state)
        finally:
            self.lock.release()
