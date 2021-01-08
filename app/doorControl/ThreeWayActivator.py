import datetime
import enum
import threading

COOL_DOWN_INTERVAL = 1
HOLD_DOWN_INTERVAL = 1


class ThreeWayActivatorStateEnum(enum.Enum):
    IDLE = "idle",
    REQUESTED = "requested",
    ACTIVE = "active",
    COOL_DOWN = "coolDown"


class ThreeWayActivatorThread(threading.Thread):

    def __init__(self, activator, progress_listener=None):
        super().__init__()
        self.state = ThreeWayActivatorStateEnum.IDLE
        self.state_changed_at = datetime.datetime.utcnow()
        self.sync_object = threading.Condition()
        self.activator = activator
        self.progressListener = progress_listener

    def switch_state_to(self, new_state: ThreeWayActivatorStateEnum):
        self.state = new_state
        self.state_changed_at = datetime.datetime.utcnow()
        if self.progressListener:
            self.progressListener(self.state)

    def seconds_passed_from_last_state_chaged(self):
        delta = (datetime.datetime.utcnow() - self.state_changed_at)
        return delta.seconds

    def run(self):
        while True:
            with self.sync_object:
                print(f"Go and check... State: {self.state}, changed {self.seconds_passed_from_last_state_chaged()} seconds ago...")
                if self.state == ThreeWayActivatorStateEnum.REQUESTED:
                    self.activator.on()
                    self.switch_state_to(ThreeWayActivatorStateEnum.ACTIVE)

                if self.state == ThreeWayActivatorStateEnum.ACTIVE \
                        and self.seconds_passed_from_last_state_chaged() >= HOLD_DOWN_INTERVAL:
                    self.activator.off()
                    self.switch_state_to(ThreeWayActivatorStateEnum.COOL_DOWN)

                if self.state == ThreeWayActivatorStateEnum.COOL_DOWN \
                        and self.seconds_passed_from_last_state_chaged() >= COOL_DOWN_INTERVAL:
                    self.switch_state_to(ThreeWayActivatorStateEnum.IDLE)

                self.sync_object.wait(timeout=1)

    def activate(self):
        with self.sync_object:
            if self.state == ThreeWayActivatorStateEnum.IDLE:
                self.state = ThreeWayActivatorStateEnum.REQUESTED
                self.sync_object.notifyAll()
