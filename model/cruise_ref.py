"""Python reference model of the cruise-control state machine.
Executable spec for back-to-back comparison against the Simulink/Stateflow model."""
from dataclasses import dataclass

OFF, STANDBY, ACTIVE, SUSPENDED = 0, 1, 2, 3
STATE_NAMES = {0: "OFF", 1: "STANDBY", 2: "ACTIVE", 3: "SUSPENDED"}
MIN_SPEED, MAX_SET = 30.0, 105.0

@dataclass
class Inputs:
    enable: int = 0
    set_sw: int = 0
    resume_sw: int = 0
    brake: int = 0
    clutch: int = 0
    speed: float = 0.0

class CruiseRef:
    def __init__(self):
        self.state, self.set_speed = OFF, 0
        self._prev_set = self._prev_resume = 0

    def step(self, i: Inputs):
        set_edge = i.set_sw and not self._prev_set
        res_edge = i.resume_sw and not self._prev_resume
        self._prev_set, self._prev_resume = i.set_sw, i.resume_sw
        free = not (i.brake or i.clutch)

        if not i.enable:                                   # REQ-CC-001
            self.state, self.set_speed = OFF, 0
        elif self.state == OFF:                            # REQ-CC-002
            self.state = STANDBY
        elif self.state == STANDBY:
            if set_edge and MIN_SPEED <= i.speed <= MAX_SET and free:   # REQ-CC-003/004/008
                self.state, self.set_speed = ACTIVE, int(round(i.speed))
        elif self.state == ACTIVE:
            if i.speed < MIN_SPEED:                        # REQ-CC-007
                self.state, self.set_speed = STANDBY, 0
            elif not free:                                 # REQ-CC-005
                self.state = SUSPENDED
        elif self.state == SUSPENDED:
            if i.speed < MIN_SPEED:                        # REQ-CC-007
                self.state, self.set_speed = STANDBY, 0
            elif res_edge and free:                        # REQ-CC-006
                self.state = ACTIVE
        if self.state in (OFF, STANDBY):                   # REQ-CC-009
            self.set_speed = 0
        return self.state, self.set_speed, int(self.state == ACTIVE)   # REQ-CC-010
