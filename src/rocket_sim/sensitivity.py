"""Local finite-difference sensitivity estimates."""
from dataclasses import dataclass
@dataclass(frozen=True)
class Sensitivity:
    parameter: str
    baseline: float
    perturbed: float
    derivative: float
    normalized: float|None
def finite_difference_sensitivity(function,value,step,parameter="parameter"):
    if step<=0: raise ValueError("step must be positive")
    center=float(function(value)); plus=float(function(value+step)); minus=float(function(value-step))
    derivative=(plus-minus)/(2*step)
    normalized=derivative*value/center if center!=0 else None
    return Sensitivity(parameter,center,plus,derivative,normalized)
def one_sided_sensitivity(function,value,step,parameter="parameter"):
    if step<=0: raise ValueError("step must be positive")
    center=float(function(value)); plus=float(function(value+step))
    derivative=(plus-center)/step
    return Sensitivity(parameter,center,plus,derivative,derivative*value/center if center else None)
