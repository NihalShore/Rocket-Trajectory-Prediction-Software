"""Reusable analysis helpers for comparing trajectory runs."""
from dataclasses import dataclass
import numpy as np
from .simulation import SimulationResult
@dataclass(frozen=True)
class Comparison:
    labels: tuple[str,...]
    peak_altitudes: tuple[float,...]
    peak_speeds: tuple[float,...]
    peak_dynamic_pressures: tuple[float,...]
def compare_results(results,labels=None):
    results=list(results)
    if not results: raise ValueError("at least one result is required")
    names=tuple(labels or [r.config.vehicle.name for r in results])
    if len(names)!=len(results): raise ValueError("label count must match result count")
    return Comparison(names,tuple(r.metrics.maximum_altitude for r in results),
                      tuple(r.metrics.maximum_speed for r in results),
                      tuple(r.metrics.maximum_dynamic_pressure for r in results))
def interpolate_at_altitude(result: SimulationResult,altitude: float):
    """Return the first rising crossing of an altitude as a dict."""
    for a,b in zip(result.samples,result.samples[1:]):
        if a.state.altitude<=altitude<=b.state.altitude and b.state.altitude>a.state.altitude:
            f=(altitude-a.state.altitude)/(b.state.altitude-a.state.altitude)
            return {"time":a.time+f*(b.time-a.time),
                    "speed":a.state.speed+f*(b.state.speed-a.state.speed),
                    "mass":a.state.mass+f*(b.state.mass-a.state.mass)}
    return None
def resample(result: SimulationResult,interval: float):
    if interval<=0: raise ValueError("interval must be positive")
    t=result.times; alt=result.altitudes
    grid=np.arange(t[0],t[-1]+interval*.5,interval)
    return {"time":grid,"altitude":np.interp(grid,t,alt),
            "downrange":np.interp(grid,t,result.downrange),
            "speed":np.interp(grid,t,result.speeds)}
