"""Adaptive Dormand-Prince integration with bounded step-size control."""
from dataclasses import dataclass
import numpy as np
from .integrators import rk45_step
@dataclass(frozen=True)
class AdaptiveResult:
    times: np.ndarray
    states: np.ndarray
    accepted_steps: int
    rejected_steps: int
    function_evaluations: int
def integrate_adaptive(fun,y0,t0,t1,initial_step,absolute_tolerance=1e-8,
                       relative_tolerance=1e-6,min_step=1e-8,max_step=float("inf"),
                       safety_factor=.9,max_steps=100000):
    if t1<t0 or initial_step<=0 or min_step<=0 or max_step<min_step:
        raise ValueError("invalid integration interval or step bounds")
    if absolute_tolerance<=0 or relative_tolerance<=0 or not 0<safety_factor<1:
        raise ValueError("invalid tolerance or safety factor")
    y=np.asarray(y0,dtype=float).copy()
    t=float(t0); h=min(initial_step,max_step,t1-t if t1>t0 else initial_step)
    times=[t]; states=[y.copy()]; accepted=0; rejected=0; evaluations=0
    for _ in range(max_steps):
        if t>=t1: break
        h=min(h,max_step,t1-t)
        candidate,error=rk45_step(fun,t,y,h); evaluations+=7
        scale=absolute_tolerance+relative_tolerance*np.maximum(np.abs(y),np.abs(candidate))
        norm=float(np.sqrt(np.mean((error/scale)**2)))
        if norm<=1.0:
            t+=h; y=candidate; times.append(t); states.append(y.copy()); accepted+=1
        else: rejected+=1
        factor=5.0 if norm==0 else safety_factor*norm**(-.2)
        factor=min(5.0,max(.1,factor))
        h=min(max_step,max(min_step,h*factor))
        if h<=min_step and norm>1.0: raise RuntimeError("adaptive solver cannot satisfy tolerance at min_step")
    else: raise RuntimeError("maximum adaptive step count exceeded")
    if t<t1: raise RuntimeError("integration ended before final time")
    return AdaptiveResult(np.asarray(times),np.asarray(states),accepted,rejected,evaluations)
