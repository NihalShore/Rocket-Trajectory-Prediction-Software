"""Telemetry channel extraction and lightweight derived series."""
import numpy as np
def channel(samples,name):
    aliases={"time":lambda s:s.time,"altitude":lambda s:s.state.altitude,
    "downrange":lambda s:s.state.downrange,"speed":lambda s:s.state.speed,
    "mass":lambda s:s.state.mass,"thrust":lambda s:s.thrust,"drag":lambda s:s.drag,
    "dynamic_pressure":lambda s:s.dynamic_pressure,"mach":lambda s:s.mach,
    "vertical_velocity":lambda s:s.state.vertical_velocity,
    "horizontal_velocity":lambda s:s.state.horizontal_velocity}
    if name not in aliases: raise KeyError(f"unknown telemetry channel: {name}")
    return np.asarray([aliases[name](s) for s in samples],dtype=float)
def finite_difference(times,values):
    t=np.asarray(times,dtype=float); v=np.asarray(values,dtype=float)
    if t.ndim!=1 or v.ndim!=1 or len(t)!=len(v) or len(t)<2: raise ValueError("matching one-dimensional arrays with at least two values are required")
    if np.any(np.diff(t)<=0): raise ValueError("times must increase")
    return np.gradient(v,t,edge_order=1)
def moving_average(values,window):
    a=np.asarray(values,dtype=float)
    if window<1 or window>len(a): raise ValueError("window must be between one and series length")
    weights=np.ones(window)/window
    return np.convolve(a,weights,mode="valid")
