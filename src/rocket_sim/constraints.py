"""Trajectory constraint evaluation and engineering margin reporting."""
from dataclasses import dataclass
@dataclass(frozen=True)
class ConstraintResult:
    name: str
    measured: float
    limit: float
    margin: float
    satisfied: bool
def upper_bound(name,measured,limit):
    if limit<0: raise ValueError("limit cannot be negative")
    return ConstraintResult(name,float(measured),float(limit),float(limit-measured),measured<=limit)
def lower_bound(name,measured,limit):
    return ConstraintResult(name,float(measured),float(limit),float(measured-limit),measured>=limit)
def evaluate_peak_constraints(result,max_q=None,max_acceleration=None,max_mach=None):
    checks=[]
    if max_q is not None: checks.append(upper_bound("dynamic_pressure",result.metrics.maximum_dynamic_pressure,max_q))
    if max_acceleration is not None: checks.append(upper_bound("acceleration",result.metrics.maximum_acceleration,max_acceleration))
    if max_mach is not None: checks.append(upper_bound("mach",result.metrics.maximum_mach,max_mach))
    return tuple(checks)
def all_satisfied(results): return all(item.satisfied for item in results)
