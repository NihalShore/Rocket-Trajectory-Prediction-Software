"""Trajectory interpolation, slicing, and derived-path operations."""
from bisect import bisect_left
from dataclasses import dataclass
from .state import State,TrajectorySample
@dataclass(frozen=True)
class InterpolatedState:
    time: float
    state: State
def interpolate_sample(samples,time):
    if not samples: raise ValueError("samples cannot be empty")
    if time<samples[0].time or time>samples[-1].time: raise ValueError("time outside trajectory")
    times=[s.time for s in samples]
    index=bisect_left(times,time)
    if index==0: return InterpolatedState(time,samples[0].state)
    if index==len(samples): return InterpolatedState(time,samples[-1].state)
    a,b=samples[index-1],samples[index]
    if b.time==a.time: return InterpolatedState(time,b.state)
    f=(time-a.time)/(b.time-a.time)
    values=[x+f*(y-x) for x,y in zip(a.state,b.state)]
    return InterpolatedState(time,State(*values))
def slice_time(samples,start,end):
    if end<start: raise ValueError("end must not precede start")
    return tuple(s for s in samples if start<=s.time<=end)
def maximum_sample(samples,channel):
    if not samples: raise ValueError("samples cannot be empty")
    getters={"altitude":lambda s:s.state.altitude,"speed":lambda s:s.state.speed,
             "dynamic_pressure":lambda s:s.dynamic_pressure,"mach":lambda s:s.mach}
    if channel not in getters: raise ValueError(f"unsupported channel: {channel}")
    return max(samples,key=getters[channel])
def minimum_sample(samples,channel):
    if not samples: raise ValueError("samples cannot be empty")
    getters={"altitude":lambda s:s.state.altitude,"speed":lambda s:s.state.speed,
             "dynamic_pressure":lambda s:s.dynamic_pressure,"mach":lambda s:s.mach}
    if channel not in getters: raise ValueError(f"unsupported channel: {channel}")
    return min(samples,key=getters[channel])
