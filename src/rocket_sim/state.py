"""State vector, trajectory sample, and event records."""
from dataclasses import dataclass
from typing import NamedTuple
class State(NamedTuple):
    downrange: float
    altitude: float
    horizontal_velocity: float
    vertical_velocity: float
    mass: float
    @property
    def speed(self): return (self.horizontal_velocity**2+self.vertical_velocity**2)**.5
    @property
    def flight_path_angle(self):
        import math
        return math.atan2(self.vertical_velocity,self.horizontal_velocity)
@dataclass(frozen=True)
class TrajectorySample:
    time: float
    state: State
    thrust: float
    drag: float
    dynamic_pressure: float
    mach: float
    stage_index: int
    event: str=""
@dataclass(frozen=True)
class Event:
    time: float
    name: str
    altitude: float
    speed: float
    mass: float
    details: dict
