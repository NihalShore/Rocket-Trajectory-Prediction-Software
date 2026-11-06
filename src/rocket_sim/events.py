"""Crossing and apogee detection helpers."""
from dataclasses import dataclass
@dataclass(frozen=True)
class Crossing:
    time: float
    value: float
    direction: str
def find_crossings(times,values,level=0.,direction="either"):
    ts=list(times); vs=list(values)
    if len(ts)!=len(vs): raise ValueError("times and values must have equal lengths")
    if direction not in {"rising","falling","either"}: raise ValueError("invalid crossing direction")
    result=[]
    for i in range(1,len(ts)):
        a=vs[i-1]-level; b=vs[i]-level
        crossed=(a<0<=b if direction=="rising" else a>0>=b if direction=="falling" else (a<0<=b or a>0>=b))
        if crossed:
            f=-a/(b-a) if b!=a else 0.
            result.append(Crossing(ts[i-1]+f*(ts[i]-ts[i-1]),level,direction))
    return result
def detect_apogee(samples):
    for a,b in zip(samples,samples[1:]):
        if a.state.vertical_velocity>0>=b.state.vertical_velocity:
            dv=a.state.vertical_velocity-b.state.vertical_velocity
            f=a.state.vertical_velocity/dv if dv else 0.
            return Crossing(a.time+f*(b.time-a.time),0.,"falling")
    return None
