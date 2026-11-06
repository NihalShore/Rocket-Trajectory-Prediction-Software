"""Piecewise-linear pitch programs for conceptual ascent studies."""
from dataclasses import dataclass
import math
@dataclass(frozen=True)
class PitchKnot:
    time: float
    angle_deg: float
class PitchProgram:
    def __init__(self,knots):
        if not knots: raise ValueError("at least one knot required")
        if any(b.time<=a.time for a,b in zip(knots,knots[1:])): raise ValueError("knot times must increase")
        if any(not 0<=k.angle_deg<=180 for k in knots): raise ValueError("pitch angle must be within [0,180]")
        self.knots=tuple(knots)
    def angle(self,time):
        if time<=self.knots[0].time: return math.radians(self.knots[0].angle_deg)
        if time>=self.knots[-1].time: return math.radians(self.knots[-1].angle_deg)
        for a,b in zip(self.knots,self.knots[1:]):
            if a.time<=time<=b.time:
                f=(time-a.time)/(b.time-a.time)
                return math.radians(a.angle_deg+f*(b.angle_deg-a.angle_deg))
        raise RuntimeError("pitch interpolation failed")
    def direction(self,time):
        a=self.angle(time); return math.cos(a),math.sin(a)
def vertical_program(): return PitchProgram([PitchKnot(0,90),PitchKnot(20,90)])
def gravity_turn_program(start_time=10.,end_time=150.,terminal_angle_deg=5.):
    if end_time<=start_time: raise ValueError("end time must exceed start time")
    return PitchProgram([PitchKnot(0,90),PitchKnot(start_time,90),PitchKnot(end_time,terminal_angle_deg)])
